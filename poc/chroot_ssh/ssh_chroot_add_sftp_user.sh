#!/bin/bash

echo "Kullanici Adini Giriniz:"
read username

echo "Kullanici Sifresini Giriniz:"
read password

/usr/sbin/adduser "$username" -d /home/"$username" -g chroot -s /bin/false
echo -e "$password\n$password" | /usr/bin/passwd "$username"

chown  root:root /home/$username
chmod  0755 /home/$username
usermod -G chroot "$username"
usermod -s /bin/false "$username"
cd /home/$username
rm -rf .bash*

mkdir report
chown "$username" report
chmod 700 report

echo "Kullanici Basarili Bir Sekilde Olusturulmustur ... "
