#!/usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
     read_file = open("dosya.txt", "r").read().splitlines()
     for line in read_file:
          print line
 
