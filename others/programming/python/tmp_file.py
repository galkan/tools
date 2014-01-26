#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
     import tempfile
except ImportError,err:
     import sys
     sys.stdout.write("%s" %err)
     sys.exit(1)


if __name__ == "__main__":
     tmp_file =  tempfile.NamedTemporaryFile(mode='w+t')
     tmp_file_name = tmp_file.name  # Dosyanın adını almak için
     tmp_file.write("text")
     tmp_file.seek(0)

     for line in tmp_file:
           print line

     tmp_file.close()
 
