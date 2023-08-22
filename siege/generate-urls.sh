#!/bin/bash
set -e

test -f sitemap.xml || wget https://www.kotipizza.fi/sitemap.xml
sed -n 's:.*<loc>\(.*\)</loc>.*:\1:p' sitemap.xml > urls.txt
