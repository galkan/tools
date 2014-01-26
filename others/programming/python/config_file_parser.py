#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
     import sys
except ImportError,e:
     import sys
     sys.stdout.write("%s\n" %e) 
     sys.exit(1)


def parse_config_file(config_file)
     if not os.path.isfile(conf_file):
          error_message = "%s Dosyasi Sistemde Bulunamadi !!!"% (conf_file)
          print >> sys.stderr, "Hata: %s"% error_message
          sys.exit(2)

     try:
         parser = SafeConfigParser()
         parser.read(conf_file)
         for section_name in parser.sections():
             if section_name == "postgresql":
                  for name, value in parser.items(section_name):
                       if name == "host":
                          host = value
                       elif name == "password":
                          password = value
                       elif name == "user":
                          user = value
                       elif name == "database":
                          database = value
  


#[postgresql]
#host = host
#database = database
#password = password
#user = user

if __name__ == "__main__":
     db_conf_file = "/etc/db.conf"
     
