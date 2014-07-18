#!/bin/bash
# Create spk files, By Galkan
 
if [ ! $# -eq 1 ]
then
	echo "Usage: $0 <scripts_dir>"
	exit 1
fi

scripts_dir="$1"
if [ ! -d "$scripts_dir" ]
then
        mkdir "$scripts_dir"
	cd "$scripts_dir"
else
        rm -rf "$scripts_dir"
        mkdir "$scripts_dir"
	cd "$scripts_dir"
fi

for cmd_name in HELP STATS RTIME LTIME SRUN TRUN GMON GDOG KSTET GTER HTER KSTAN EXIT
do
	_file_name="`echo "$cmd_name" | tr [A-Z] [a-z]`"
	file_name="$_file_name.spk"

	echo "printf(\"$cmd_name -> $file_name: \");" > $file_name
	echo "s_readline();" >> $file_name
	echo "s_string(\"$cmd_name \");" >> $file_name
	echo "s_string_variable(\"COMMAND\");" >> $file_name
done

exit 0
