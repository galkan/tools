#!/bin/bash

send_tcp="/usr/bin/generic_send_tcp"

target="$1"
port="$2"
spk="$3"

if [ ! $# -eq 3 ]
then
	echo "Usage: $0 <target> <port> <spk>"
	exit 1
fi

$send_tcp  $target $port $spk 0 0
