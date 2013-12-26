#!/bin/bash
# By Galkan 

if [ ! $# -eq 2 ]
then
  echo "Kullanim: $0 <domain_name> <mail_adresi>"
  exit 1
fi

function send_report()
{
        email_to="$1"
        email_content="$2"

        tmp_mail="`mktemp /tmp/$USER.XXXXXX`"
        echo "From: <Defacements Report> defacements@agguvenligi.net" >> $tmp_mail
        echo "Subject: Defacements Report" >> $tmp_mail
        echo "To:  $email_to" >> $tmp_mail
        echo "Content-type: text/plain;charset=\"utf-8\"" >> $tmp_mail
        cat "$email_content" >> $tmp_mail
        cat $tmp_mail  |  /usr/sbin/sendmail  $email_to

        rm -f  $tmp_mail
}


domain="$1"
email_to="$2"
zoneh_url="http://www.zone-h.org/rss/defacements"
output_file="`mktemp /tmp/$USER.XXXXXX`"

wget "$zoneh_url" -O $output_file  2>/dev/null
control=0

cat $output_file  | while read -r line
do

	echo "$line" | grep -Eq "<title>.*https?://.*$domain"
	if [ $? -eq 0 ]
	then
		host="`echo "$line" | cut -d "[" -f3 | cut -d "]" -f1`"
		control=1
	fi


	if [ $control -eq 1 ]
	then
		echo "$line" | grep -q "<link>"
		if [ $? -eq 0 ]
		then	
			link="`echo "$line" | cut -d "[" -f3 | cut -d "]" -f1`"
			control=2
		fi
	fi

	
	if [ $control -eq 2 ]
	then
		echo "$line" | grep -q "<pubDate>"
		if [ $? -eq 0 ]
		then
			pubdate="`echo "$line" | cut -d ">" -f2- | cut -d "<" -f1 | cut -d " " -f1-5`"
			control=0
			
			output_file="`mktemp /tmp/$USER.XXXXXX`"
			echo "--- Defacements Reports --- " >> $output_file
			echo "link: $link" >> $output_file
			echo "host: $host" >> $output_file
			echo "pubdate: $pubdate" >> $output_file

			cat $output_file

			send_report "$email_to" "$output_file"
			rm -f $output_file
		fi
	fi

done

rm -rf $output_file
