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

keywords = ["unit", "uses", "begin", "Boolean", "function", "procedure", "implementation", "type", "shl", "shr", "to", "until", "uses", "while", "False", "True", "else", "do", "and"]

unary = ["+","-","*","shl","shr"]

def checkunitname(fileName):
    with open(fileName, "r") as f:
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

def isacomment(line):
    return line.startswith('//')

def checkforkeywords(fileName):
    with open(fileName, "r") as f:
        nrline = 1
        while 1:
            line = f.readline()
            if not line: break
            if isacomment(line.lstrip()):
                nrline += 1
                continue
            for keyw in keywords:
                myregx = r"\s+" + keyw.upper() +r"\s" + r"|" + r"^" + keyw.upper() + r"\s"
                if re.search(myregx, line.upper()):
                    # TODO: to check all the occurrences
                    if line.find(keyw) == -1:
                        i = line.upper().find (keyw.upper())
                        print(fileName + '(' + str(nrline) + ',' + str(i+1) + ')' + ' Note: the reserved word <' + keyw + '> must be in lower case')
            # Tabs are not allowed
            if re.search (r'\t', line):
                print(fileName + '(' + str(nrline) + ',' + str(1) + ')' + ' Note: tab found!')
            nrline += 1

def checkunaryoperators(fileName):
    with open(fileName, "r") as f:
        nrline = 1
        while 1:
            line = f.readline()
            if not line : break
            if isacomment (line.lstrip()):
                nrline += 1
                continue
            for uny in unary:
                result = line.find(uny)
                if (result != -1) and (line[result-1] == ' ') or (line[result+1] == ' '):
                    print(fileName + '(' + str(nrline) + ','+ str(result) +')' + ' Note: unary operators do not need blanks between its operands')
            nrline += 1

def checkequal(fileName):
    with open(fileName, "r") as f:
        nrline = 1
        while 1:
            line = f.readline()
            if not line : break
            if isacomment (line.lstrip()):
                nrline += 1
                continue
            result = line.find(':=')
            if (result != -1):
                if line[result - 1] != ' ' or line[result + 2] != ' ':
                    print(fileName + '(' + str(nrline) + ','+ str(result+1) +')' + ' Note: := must be surrounded by blanks')
            nrline += 1

def checkcomablanks(fileName):
    with open(fileName, "r") as f:
        nrline = 1
        while 1:
            line = f.readline()
            if not line : break
            if isacomment (line.lstrip()):
                nrline += 1
                continue
            result = line.find(',')
            if (result != -1):
                if line[result + 1] != ' ':
                    print(fileName + '(' + str(nrline) + ','+ str(result+1) +')' + ' Note: blank missed after ,')
            nrline += 1

# TODO: keywords in strings should be ignored
checkforkeywords(sys.argv[1])

# unit name must be the same as the name used by the operating system's file system
checkunitname(sys.argv[1])

# blanks should not be used between a unary operator and its operand
checkunaryoperators(sys.argv[1])

# the ':=' operator must surrounded by blanks
checkequal(sys.argv[1])

## ',' must be followed by a blank
checkcomablanks(sys.argv[1])

## TODO: add a warning to detect "if%b(/W)%b"
