#!/usr/bin/python

import os, sys

def main(args):
    if len(args) != 2:
        print "Usage: %s start|stop|restart" % args[0]
        exit(-1)
    method = args[1]
    if method == 'start':
        os.system("""
cd /home/distribution
gunicorn distribution.wsgi:application &
python manage.py celery worker > /dev/null 2>&1&""")
    elif method == 'stop':
        os.system("kill -9 `ps -ef | grep gunicorn | grep -v grep | awk '{if(NR==1) print $2}'`")
        os.system("kill -9 `ps -ef | grep celery | grep worker | grep -v grep | awk '{if(NR==1) print $2}'`")
    elif method == 'restart':
        os.system("kill -9 `ps -ef | grep gunicorn | grep -v grep | awk '{if(NR==1) print $2}'`")
        os.system("kill -9 `ps -ef | grep celery | grep worker | grep -v grep | awk '{if(NR==1) print $2}'`")
        os.system("sleep 5")
        os.system("""
cd /home/distribution
gunicorn distribution.wsgi:application &
python manage.py celery worker > /dev/null 2>&1& """)
    else:
        print "Usage: %s start|stop|restart" % args[0]
        exit(-1)

if __name__ == '__main__':
    main(sys.argv)
