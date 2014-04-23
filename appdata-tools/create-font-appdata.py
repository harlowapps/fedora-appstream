#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License Version 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2013
#    Richard Hughes <richard@hughsie.com>
#

import csv
import sys

def main():

    csvfile = open('./fonts.csv', 'r')
    data = csv.reader(csvfile)

    old_name = None
    old_summary = None

    for row in data:

        if row[0].startswith('AppStream ID'):
            continue

        #font = FontCollection()
        font_id = row[0]
        parent = row[1]
        classifier = row[2]
        name = row[3]
        summary = row[4]

        if len(name) == 0:
            print "WARNING", font_id, "missing name using", font_id
            continue
        if len(summary) == 0:
            print "WARNING", font_id, "missing summary"
            continue

        # save
        if name == '^':
            name = old_name
        else:
            old_name = name
        if summary == '^':
            summary = old_summary
        else:
            old_summary = summary

        filename = '../appdata-extra/font/' + font_id.rsplit('.', 2)[0] + '.appdata.xml'
        txt = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        txt += "<application>\n"
        txt += "  <id type=\"font\">%s</id>\n" % font_id
        txt += "  <licence>CC0</licence>\n"
        if len(name) > 0:
            txt += "  <name>%s</name>\n" % name
        if len(summary) > 0:
            txt += "  <summary>%s</summary>\n" % summary
        if len(classifier) > 0 or len(parent) > 0:
            txt += "  <metadata>\n"
            if len(classifier) > 0:
                txt += "    <value key=\"FontClassifier\">%s</value>\n" % classifier
            if len(parent) > 0:
                txt += "    <value key=\"FontParent\">%s</value>\n" % parent
            txt += "  </metadata>\n"
        txt += "</application>\n"
        f = open(filename, 'w')
        f.write(txt)
        f.close()

    csvfile.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
