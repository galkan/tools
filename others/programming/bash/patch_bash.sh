#!/bin/sh
 
version="4.2"
nodotversion="42"
lastpatch="53"
 
for i in `seq 1 $lastpatch`;
do
    number=$(printf %02d $i)
    file="https://ftp.gnu.org/pub/gnu/bash/bash-${version}-patches/bash${nodotversion}-0$number"
    curl -k $file | patch -N -p0
done
