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


class Command(BaseCommand):
    help = 'Generate a blog post report of Box folder sizes'

    def handle(self, *args, **options):
        os.chdir('/Box')
        try:
            # Run du against all top-level directories in the RBG-Shared Box Folder, 1 directory deep
            for line in subprocess.check_output(['du', '-d', '1'] + glob.glob('*')[:2], encoding='utf-8').split(
                    sep="\n"):
                line = line.split(sep='\t')
                if len(line) < 2:
                    # The last item of the output will [''] so we avoid an IndexError by checking the list length
                    continue
                print("Line:", line)
                print("[*] Saving {} with size {}...".format(line[1], line[0]))
                folder, created = Folder.objects.get_or_create(name=line[1])
                folder.save()
                stat = FolderStats(folder=folder, size=int(line[0]))
                stat.save()
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
        # TODO - Get total disk usage by department and add to blog report paragraph
        body = json.dumps([
            {u'type': u'heading', u'value': u'Department Breakdown By Disk Usage'},
            {u'type': u'paragraph', u'value': u'test'},
        ])
        new_post = BlogPage(
            title=title,
            draft_title=title,
            slug=title.replace(' ', '-'),
            show_in_menus=True,
            content_type=blogpage_content_type,
            author=get_user_model().objects.get(username='intranet_admin'),
            summary='Disk usage report for top-level Box folders generated on ' + today,
            body=body,
        )
        parent_page.add_child(instance=new_post)
        new_post.categories.add(category)
        new_post.save()
