#!/usr/bin/python

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '2013'


try:
        import sys
        import os
        import time
        import atexit
        from signal import SIGTERM
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class Daemon(object):

        def __init__ (self, pidfile, stdin="/dev/null", stdout="/dev/null", stderr="/dev/null"):
                self.pidfile = pidfile
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr


        def daemonize (self):
                try:
                        pid = os.fork()
                        if pid >0:
                                sys.exit(0)
                except OSError,e:
                        sys.stderr.write("Fork 1 Failed %d %s" % (e.errno,e.strerror))
                        sys.exit(1)

                os.chdir("/")
                os.setsid()
                os.umask(0)

                try:
                        pid = os.fork()
                        if pid >0:
                                sys.exit(0)
                except OSError,e:
                        sys.stderr.write("Fork 2 Failed %d %s" % (e.errno,e.strerror))
                        sys.exit(1)

                sys.stdout.flush()
                sys.stderr.flush()

                si = file(self.stdin,"r")
                so = file(self.stdout, "a+")
                se = file(self.stderr, "a+", 0)
                os.dup2(si.fileno(),sys.stdin.fileno())
                os.dup2(so.fileno(),sys.stdout.fileno())
                os.dup2(se.fileno(),sys.stderr.fileno())

                atexit.register(self.removepid)
                pid = int(os.getpid())
                file(self.pidfile,"w+").write("%s\n" % pid)


        def removepid (self):
                os.remove(self.pidfile)


        def start (self):
                try:
                        f = file(self.pidfile,"r")
                        pid = int(f.read().strip())
                        f.close()
                except IOError:
                        pid = None

                if pid:
                        sys.stderr.write("Daemon Already Running !!!\n")
                        sys.exit(1)

                self.daemonize()
                self.run()


        def stop (self):
                try:
                        f = file(self.pidfile,"r")
                        pid = int(f.read().strip())
                        f.close()
                except IOError:
                        pid = None

                if not pid:
                        sys.stderr.write("Daemon Not Running !!!\n")
                        return

                try:
                        while True:
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError,err:
                        error = str(err)
                        if error.find("No such process"):
                                os.system("pkill program.py")

                                if os.path.exists(self.pidfile):
                                        os.remove(self.pidfile)
                                        sys.exit(0)

                        else:
                                print error
                                sys.exit(1)


        def run (self):
                """ Override This Function"""

 

class Deneme (Daemon):
        def run(self):
                while True:
                        print "Daemon Olarak Calisiyorum Ben"
                        time.sleep(1)


if __name__ == "__main__":
        daemon_pid = "/var/run/daemon.pid"
        deneme_daemon  = Deneme(daemon_pid)
        deneme_daemon.start()
