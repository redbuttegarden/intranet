import datetime
import glob
import json
import os
import subprocess
import time

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from blog.models import BlogPage, BlogCategory, BlogIndexPage
from box.models import Folder, FolderStats

DEPARTMENT_FOLDERS = {'Administration': ['Accounting', 'Administration', 'Administration - Archive', 'Concerts',
                                         'Projects', 'Projects - Archive'],
                      'Communications': ['Communications', 'Communications - Archive'],
                      'Conservation': ['Conservation', 'Conservation - Archive', 'RANA Videos - Conservation'],
                      'Development': ['Development', 'Development - Archive', 'ZAP'],
                      'Horticulture': ['Horticulture', 'Horticulture - Archive', 'Photo Library - Plant Records',
                                       'Plant Records', 'Plant Records - Archive'],
                      'Information Technology': ['Box Demo', 'IT', 'IT - Archive', 'IT - Software Images'],
                      'Miscellaneous': ['Homes', 'Photo Library', 'Shared', 'Volunteer'],
                      'Programs': ['Programs', 'Programs - Admin', 'Programs - Release Forms Archive',
                                   'Programs-Archive'],
                      'Visitor Services': ['Visitor Services', 'Visitor Services - Archive']}


class Command(BaseCommand):
    help = 'Generate a blog post report of Box folder sizes'

    def handle(self, *args, **options):
        # Dictionary to store aggregate disk usage info based
        du_dept_dict = {}
        os.chdir('/Box')
        try:
            # Run du against all top-level directories in the RBG-Shared Box Folder, 1 directory deep
            for line in subprocess.check_output(['du', '-d', '1'] + glob.glob('*'), encoding='utf-8').split(
                    sep="\n"):
                line = line.split(sep='\t')
                if len(line) < 2:
                    # The last item of the output will be [''] so we avoid an IndexError by checking the list length
                    continue
                print("Line:", line)
                folder_size = int(line[0])
                folder_name = line[1]
                print("[*] Saving {} with size {}...".format(folder_name, folder_size))
                folder, created = Folder.objects.get_or_create(name=line[1])
                folder.save()
                stat = FolderStats(folder=folder, size=int(line[0]))
                stat.save()

                # If folder is top-level (no subfolder), add to total disk usage for that department
                if '/' not in folder_name:
                    # Determine which department this folder belongs to
                    department = get_department_by_folder(DEPARTMENT_FOLDERS, folder_name)
                    try:
                        du_dept_dict[department] += folder_size
                    except KeyError:
                        du_dept_dict[department] = folder_size

        except subprocess.CalledProcessError as e:
            print("[!]", e)
            if 'Network is unreachable' in str(e):
                time.sleep(10)  # Wait 10 seconds for the network

        parent_page = BlogIndexPage.objects.get(slug='it-blog')
        category = BlogCategory.objects.get(name='Inventory')
        blogpage_content_type = ContentType.objects.get_for_model(
            BlogPage
        )
        today = str(datetime.date.today())
        title = 'Box Folder Report ' + today
        body = json.dumps([
            {u'type': u'heading', u'value': u'Department Breakdown By Disk Usage'},
            {u'type': u'paragraph', u'value': generate_body(du_dept_dict)},
        ])
        # We use get_or_create so box_report can be run more than once in a single day without throwing an error
        new_post, created = BlogPage.objects.get_or_create(
            slug=title.replace(' ', '-'),
        )
        new_post.title = title
        new_post.draft_title = title
        new_post.show_in_menus = True
        new_post.content_type = blogpage_content_type
        new_post.author = get_user_model().objects.get(username='intranet_admin')
        new_post.summary = 'Disk usage report for top-level Box folders generated on ' + today
        new_post.body = body
        if created:
            parent_page.add_child(instance=new_post)
        new_post.categories.add(category)
        new_post.save()


def generate_body(du_dept_dict):
    """Return HTML that will be used for the body content of the box report BlogPage"""
    body = '<ul>'
    for item in du_dept_dict.items():
        body += '<li>{}: {} GB</li>'.format(item[0], int(item[1]) / 1000000)  # Convert to GB
    body += '</ul>'
    return body


def get_department_by_folder(department_folder_dict, folder_name):
    department_folders = department_folder_dict.items()
    for item in department_folders:
        if folder_name in item[1]:
            return item[0]

    raise ValueError('[!] {} not found in list of department folders! You may need to add this folder to the '
                     'DEPARTMENT_FOLDERS variable in the box_report management command.'.format(folder_name))
