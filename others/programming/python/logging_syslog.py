#!/usr/bin/python

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '2013'


try:
        import logging
        import logging.handlers
        import sys
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class Log:
        logger = None

        @staticmethod
        def log_message(level, message):
                if not Log.logger:
                        Log.logger = logging.getLogger("Galkan")
                        syslog_handler = logging.handlers.SysLogHandler( address = ( '127.0.0.1', 514 ), facility = logging.handlers.SysLogHandler.LOG_LOCAL5 )
                        formatter = logging.Formatter('[%(levelname)s] - %(message)s')
                        syslog_handler.setFormatter(formatter)
                        Log.logger.addHandler( syslog_handler )

                if level == 1:
                        Log.logger.setLevel( logging.INFO )
                        Log.logger.info(message)
                elif level == 2:
                        Log.logger.setLevel( logging.WARN )
                        Log.logger.warn(message)
                elif level == 3:
                        Log.logger.setLevel( logging.ERROR )
                        Log.logger.error(message)



if __name__ == "__main__":
     Log.log_message(1, "Mesaj")


# vi /etc/rsyslog.conf     
# $UDPServerAddress 127.0.0.1
# $UDPServerRun 514
# local5.info                             -/var/log/galkan.log
# /etc/init.d/rsyslog restart
