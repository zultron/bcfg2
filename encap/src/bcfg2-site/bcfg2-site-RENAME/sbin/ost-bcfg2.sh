#!/bin/sh

#
# ost-bcfg2.sh : Control bcfg2 client via ostiary (wrapper script)
# $Id$
#

umask 002
exec 2>&1

PATH=/usr/local/lib/bcfg2/bin:/usr/local/bin:/usr/bin:/bin
PYTHONPATH="/usr/local/lib/bcfg2/lib/python2.4:/usr/local/lib/bcfg2/lib/python2.4/site-packages:/usr/local/lib/bcfg2/lib/python2.4/site-packages/Bcfg2"
export PATH PYTHONPATH

LOGDIR="/usr/local/var/svlogd/bcfg2-client-ostiary"
test -d $LOGDIR || mkdir $LOGDIR
LOG="svlogd -tt $LOGDIR"

case $0 in
       *-dvqn) bcfg2 -d -v -q -n       | $LOG ;;
        *-dvn) bcfg2 -d -v -n          | $LOG ;;
        *-dvq) bcfg2 -d -v -q          | $LOG ;;
         *-dv) bcfg2 -d -v             | $LOG ;;
         *-vq) bcfg2 -v -q             | $LOG ;;
          *-v) bcfg2 -v                | $LOG ;; 
    *-restart) sv restart bcfg2-client | $LOG ;; 
            *) printf "ERROR in $0\n"  | $LOG ;; 
esac

exit 0
