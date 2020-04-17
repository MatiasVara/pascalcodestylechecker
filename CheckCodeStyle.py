#!/usr/bin/python
# CheckCodeStyle.py
#
# CheckCodeStyle.py is a simple script to check the code style of pascal files
# See https://edn.embarcadero.com/article/10280
#
# Copyright (c) 2003-2020 Matias Vara <matiasevara@gmail.com>
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import sys
import re
import os

keywords = ["unit", "uses", "begin", "function", "procedure", "implementation", "type", "shl", "shr", "to", "until", "uses", "while", "false", "true", "else", "do", "and"]


def checkunitname(fileName):
    f = open (fileName, 'r')
    fileonly = re.search(r"(.+?).pas", os.path.basename(fileName))
    nrline = 1
    while 1:
        line = f.readline()
        if not line : break
        if isacomment (line.lstrip()):
            nrline += 1
            continue
        s = re.search(r"(?<=unit\s)\w+", line)
        if s:
            if not s.group(0) in fileonly.group(1):
                print(fileName + '(' + str(nrline) + ',1)' + ' Note: Unit name and filename must be the same')
            break
        nrline += 1
    f.close();

def isacomment(line):
    return line.startswith('//')

def checkforkeywords(fileName):
    f = open (fileName, 'r')
    nrline = 1
    while 1:
        line = f.readline()
        if not line: break
        if isacomment(line.lstrip()):
            nrline += 1
            continue
        for keyw in keywords:
            myregx = r"\W*" + keyw.upper() +r"\W"
            if re.search(myregx, line.upper()):
                # TODO: to check all the ocurrences
                if line.find(keyw) == -1:
                    i = line.upper().find (keyw.upper())
                    print(fileName + '(' + str(nrline) + ',' + str(i+1) + ')' + ' Note: the reserved word <' + keyw + '> must be in lower case')
        # Tabs are not allowed
        if re.search (r'\t', line):
            print(fileName + '(' + str(nrline) + ',' + str(1) + ')' + ' Note: tab found!')
        nrline += 1
    f.close();

# keywords must be in lowercase
checkforkeywords(sys.argv[1]);

# unit name must be the same than the filename
checkunitname(sys.argv[1]);
