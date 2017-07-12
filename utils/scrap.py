#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 baptbeuns <baptbeuns@father>
#
# Distributed under terms of the MIT license.

import subprocess
import requests
from StringIO import StringIO
from lxml import etree, html

def make_soup(url):
    if "google" in url:
        cmd = ['phantomjs', '/home/reminiz/phantomjs/utils/getGooglePage.js', url] 
        print("Initializing proc")
        err = "start"
        while err != "":
            print("proc OK. starting communicate")
            out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(out), parser)
        # page = requests.get(url)
        # tree = etree.fromstring(page.content)
    else:
        parser = etree.HTMLParser(encoding='utf8')
        tree   = etree.parse(url, parser)

    return tree

