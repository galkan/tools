Syn-Proxy
===============



     # iptables -A OUTPUT -p tcp --tcp-flags RST RST -s Syn_Proxy_Calisan_Ip -d  Nmap_Calistirilan_Ip -j DROP

Goruldugu gibi gerekli iptables kuralinin belirtiminin gerceklestirilmesinin ardindan nmap taramasi yapildiginda tum portlar acik olarak raporlanmaktadir.

    # nmap  -n -sS --open -p 10-50 192.168.6.10
    Starting Nmap 5.21 ( http://nmap.org ) at 2014-01-12 23:26 EET
    Nmap scan report for 192.168.6.10
    Host is up (0.080s latency).
    PORT   STATE SERVICE
    10/tcp open  unknown
    11/tcp open  systat
    12/tcp open  unknown
    13/tcp open  daytime
    14/tcp open  unknown
    15/tcp open  netstat
    16/tcp open  unknown
    17/tcp open  qotd
    18/tcp open  unknown
    19/tcp open  chargen
    20/tcp open  ftp-data
    21/tcp open  ftp
    22/tcp open  ssh
    23/tcp open  telnet
    24/tcp open  priv-mail
    25/tcp open  smtp
    26/tcp open  rsftp
    27/tcp open  nsw-fe
    28/tcp open  unknown
    29/tcp open  msg-icp   
    30/tcp open  unknown
    31/tcp open  msg-auth
    32/tcp open  unknown
    33/tcp open  dsp
    34/tcp open  unknown
    35/tcp open  priv-print
    36/tcp open  unknown
    37/tcp open  time
    38/tcp open  rap
    39/tcp open  unknown
    40/tcp open  unknown
    41/tcp open  unknown
    42/tcp open  nameserver
    43/tcp open  whois
    44/tcp open  mpm-flags
    45/tcp open  mpm
    46/tcp open  unknown
    47/tcp open  ni-ftp
    48/tcp open  auditd
    49/tcp open  tacacs
    50/tcp open  re-mail-ck
    MAC Address: 00:0C:29:F3:89:A1 (VMware)
