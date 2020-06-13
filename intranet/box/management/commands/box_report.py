import glob
import os
import subprocess
import time

from django.core.management.base import BaseCommand, CommandError

from blog.models import BlogPage
from box.models import Folder, FolderStats


class Command(BaseCommand):
    help = 'Generate a blog post report of Box folder sizes'

    def handle(self, *args, **options):
        os.chdir('/Box')
        try:
            for line in subprocess.check_output(['du', '-d', '1'] + glob.glob('*'), encoding='utf-8').split(sep="\n"):
                line = line.split()
                if len(line) == 0:
                    continue
                print("[*] Saving {} with size {}...".format(line[1], line[0]))
                folder, created = Folder.objects.get_or_create(name=line[1])
                folder.save()
                stat = FolderStats(folder=folder, size=int(line[0]))
                stat.save()
        except subprocess.CalledProcessError as e:
            print("[!]", e)
            if 'Network is unreachable' in str(e):
                time.sleep(10)  # Wait 10 seconds for the network
