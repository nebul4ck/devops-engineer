#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

from pathlib import Path

import os
import re

path = "."

def ls3(path):
    num = 0
    for file in Path(path).iterdir():
        if file.is_file():

            name = num+1

            print(name)

            file_name, file_ext = os.path.splitext(file)

            if re.match('^.[Jj][Pp][Gg]?', file_ext):

                newfilename = path+'/'+str(name)+'.jpg'
                os.rename(str(file),newfilename)

            elif re.match('^.[Pp][Nn][Gg]', file_ext):

                newfilename = path+'/'+str(name)+'.png'
                os.rename(str(file),newfilename)

        num = name

ls3(path)