#!/usr/bin/python

import subprocess

cmd = ['ls -la /tmp']
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

for line in iter(proc.stdout.readline, ''):
        print line[:-1]
