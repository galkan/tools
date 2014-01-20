ssh-block
=====

Oncelikle gerekli kutuphane ve programlarin sisteme kurulmasi gerekmektedir. Bunun icin paket yonetim sistemi kullanilir. Debian tabanli sistemler icin apt-get paket yonetim sistemi ile bu islem asagidaki sekilde gerceklestirilebilir. 

    # apt-get install python-scapy
    # apt-get install dsniff

whitelist ozelligi ile belirlenen ip adresleri icin ssh protokolunu tanima ozelligi kaldirilabilir. -w parametresinin ardindan belirtilen dosya icerisinde her bir satirda bir ip adresi yer alacak sekilde belirtimlerin gerceklestirilmesi gerekmektedir. ssh-block calistirmak icin genel format asagida gosterildigi gibi olmaktadir. 

    # ./ssh-block.py -c start -i eth0 -w whitelist

