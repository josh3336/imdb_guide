#!/usr/bin/env python

import os
import sys


if __name__ == "__main__":
    sys.path.append('C:/Users/josh/Documents/coding/django_stuff/testsite2/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite2.settings")


    from titles.models import Titles

    titles = Titles.objects.order_by('imdb_score')
    print titles
