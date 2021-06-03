#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

from pathlib import Path

import uuid
import os
import re

path = "."

def ls3(path):
    for file in Path(path).iterdir():
        if file.is_file():

            newuuid = str(uuid.uuid4())
            uuidname = newuuid.split('-',)[4]

            print(file)

            file_name, file_ext = os.path.splitext(file)

            if re.match('^.[Jj][Pp][Gg]?', file_ext):

                newfile = path+'/'+uuidname+'.jpg'
                os.rename(str(file),newfile)

            elif re.match('^.[Pp][Nn][Gg]', file_ext):

                newfile = path+'/'+uuidname+'.png'
                os.rename(str(file),newfile)

            print(newfile)

ls3(path)
