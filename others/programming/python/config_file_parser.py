#!/usr/bin/python

try:
        import sys
        import os
        from ConfigParser import SafeConfigParser
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


def parse_config_file(config_file):
        """

        """

        if not os.path.isfile(config_file):
                error_message = "%s Dosyasi Sistemde Bulunamadi !!!"% (config_file)
                print >> sys.stderr, "Hata: %s"% error_message
                sys.exit(1)

        result = {}
        result_line = ("host","password","user", "database")

        try:
                parser = SafeConfigParser()
                parser.read(conf_file)
                for section_name in parser.sections():
                        if section_name == "postgresql":
                                for name, value in parser.items(section_name):
                                        if name == "host":
                                                result["host"] = value
                                        elif name == "password":
                                                result["password"] = value
                                        elif name == "user":
                                                result["user"] = value
                                        elif name == "database":
                                                result["database"] = value
                for line in result_line:
                        if not line in result.keys():
                                result[line] = "-"

                return result
except Exception, err:
                print >> sys.stderr, err
                sys.exit(1)


if __name__ == "__main__":
        try:
                conf_file = sys.argv[1]
        except:
                print >> sys.stderr, "Komut Satiri Argumani Eksik !!!"
                sys.exit(1)

        for val in parse_config_file(conf_file).keys():
                print val,parse_config_file(conf_file)[val]

#[postgresql]
#host = 127.0.0.1
#database = user_pass
#passsword = Test12345
#user = deneme
