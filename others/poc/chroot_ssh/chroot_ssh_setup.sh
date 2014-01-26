#!/bin/bash


scp_path="/usr/bin/scp"
rssh_path="/usr/bin/rssh"
sftp_path="/usr/bin/sftp"
sftp_server="/usr/libexec/openssh/sftp-server"

function chroot_ssh ()
{
     tmp_file="`mktemp /tmp/$USER.XXXXXX`"
     chroot_path="$1"

     mkdir -p $chroot_path/{dev,etc,home,lib/tls,usr/{bin,lib,libexec/openssh}}
     mknod -m 666 $chroot_path/dev/null c 1 3

     for chroot_file in /etc/ld.so.cache /etc/ld.so.conf /etc/nsswitch.conf /etc/hosts /etc/resolv.conf $scp_path $rssh_path $sftp_path $sftp_server
     do
          cp "$chroot_file" "$chroot_path/$chroot_file"
     done

     for ldd_file in $scp_path $rssh_path $sftp_path $sftp_server
     do
          ldd $ldd_file | awk '{print $3}' | grep -Ev "^\("
          ldd $ldd_file | grep "ld-linux" | awk '{print $1}'
     done | sort -n | uniq | grep -Ev "^$" >> $tmp_file

     cat $tmp_file | while read -r copy_file
     do
          cp "$copy_file" "$chroot_path/$copy_file"
     done

     rm -rf $tmp_file
     chown -R root:chroot "$chroot_path"
     chmod -R 550 "$chroot_path"
     chown -R root:root "$chroot_path/etc"
     chmod 570 "$chroot_path/home"
}

function main ()
{

     chroot_path="$1"

     if [ -d "$chroot_path" ]
     then
          echo "Boyle bir dizin sistemde mevcut, silmek istiyormusunuz ? [E\H]"
          read answer

          if [ "$answer" == "E" -o "$answer" == "e" ]
          then
               rm -rf $chroot_path
               chroot_ssh "$chroot_path"
          elif [ "$answer" == "H" -o "$answer" == "h" ]
          then
               echo "Betikten Cikiliyor ..."
               exit 2
          else
               echo "[E/H] Belirtilmedi Betikten Cikiliyor"
               exit 3
          fi
      else
          chroot_ssh "$chroot_path"

      fi
}


if [ ! $# -eq  1 ]
then
     echo "Kullanim: $0 chroot_dizini"
     exit 1
else
     if [ "`echo "$1" | grep -E ".*\/$"`" ]
     then
          chroot_path="`echo "$1" | sed -e "s/\/$//g"`"
          main "$chroot_path"
     else
          main "$1"
     fi
fi
