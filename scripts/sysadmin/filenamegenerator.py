#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from pathlib import Path

import uuid
import os

path = ""

def ls3(path):
    for file in Path(path).iterdir():
        if file.is_file():

            newuuid = str(uuid.uuid4())
            uuidname = newuuid.split('-',)[4]
            newfile = path+'/'+uuidname+'.jpg'

            print file
            os.rename(str(file),newfile)
            print newfile

ls3(path)
