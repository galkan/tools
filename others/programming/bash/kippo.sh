#!/bin/bash 
# 
# Kippo Start Stop Script 
# 
# chkconfig: 345 80 20 
# description: Control Kippo 

kippo_home="/usr/local/kippo"
kippo_cfg="/usr/local/kippo/kippo.cfg"
kippo_log="/usr/local/kippo/log/kippo.log"
kippo_pid_file="/usr/local/kippo/kippo.pid"
kippo_tac="/usr/local/kippo/kippo.tac"
kippo_user="kippo"

if [ ! -f "$kippo_cfg" ] 
then 
  echo "Kippo Startup: Cannot Start" 
  exit 1 
fi 

kippo_port="`cat $kippo_cfg | grep -Ev "^#|^$" | grep ssh_port | awk '{print $3}'`"
if [ -z $kippo_port ]
then
  echo "You must set kippo port in $kippo_cfg"
  exit 2
fi

current_dir="`pwd`"

is_kippo_running()
{
  ps -ef | grep twistd | grep -q "kippo.tac" 
  if [ $? -eq 0 ]
  then
        netstat -na | grep LISTEN | grep -q "$kippo_port"
        if [ $? -eq 0 ]
        then
            return 0
        else
            return 1
        fi
  else
        return 1
  fi
}


case "$1" in 
'start') 
  is_kippo_running
  if [ $? -eq 0 ]
  then
        echo "Kippo is Already Running. PID `cat $kippo_pid_file`"
        exit 3
  else
        echo "Kippo Is Starting ..."
        cd $kippo_home
        su -c "twistd -y $kippo_tac -l $kippo_log --pidfile $kippo_pid_file" -s /bin/sh $kippo_user 1>&2 > /dev/null
        cd $current_dir
  fi         
;; 
'stop') 
  is_kippo_running
        if [ $? -eq 0 ]
        then
        echo "Kippo Is Stopping ..."
        kill -9 `cat $kippo_pid_file`
        rm -rf $kippo_pid_file
  else
        echo "Kippo Isnot Running !!!"
        exit 4  
  fi
;; 
'status')
  is_kippo_running
        if [ $? -eq 0 ] 
        then
        echo "Kippo Is Running : PID `cat $kippo_pid_file`"
        else
        echo "Kippo Is Not Running"
        fi

;;
*) 
echo "Usage: $0 { start | stop | status}" 
exit 5
;; 
esac 

exit 0 
