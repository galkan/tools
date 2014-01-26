#!/bin/bash

function check_user()
{

     username="$1"

     if [ "`grep -E "^$username:" /etc/passwd | wc -l`" -eq 1 ]
     then
         echo 1
    fi
}


function main ()
{
     echo "Silmeak Istedigini Kullanici Adini Giriniz:"
     read username

     if [ "`check_user "$username"`" == 1 ]
     then
          echo "Ev Dizininide Silmek Istiyormusunuz ? [E/Whatever You want :)]"
          read answer2
    
          if [ "$answer2" == "E" ]
          then
              userdel "$username"
              rm -rf /home/$username
              rm -rf /var/spool/mail/$username
          else
              userdel "$username"
              rm -rf /var/spool/mail/$username
          fi
     else

     echo "Boyle Bir Kullanici Bulunamadi. Yeniden Denemek Istermisiniz [E/Whatever you want :)]"
     read answer

     if [ "$answer" == "E" ]
     then
         main
     else
         exit 1
     fi
fi
}

main
