#!/bin/sh

pos=0
n=0
sp="$1"
what="$2"
found=0

[ -e /proc/sys/dev/cdrom/info ] || exit 1

/bin/awk "BEGIN { ok=0 } 
		/drive name:/ {
			gsub(/^.*:/, NIL)
			for (i=1;i<=NF;i++) {
			    c[\$i]=i
			}
		}
		/^Can.*$what:/ {
			gsub(/^.*:/, NIL, \$0)
			q=int(c[\"$sp\"])
			if (\$q == 1) {
			    ok=1
			}
		}
		END {
			if (ok) {
			    exit 0 
			} else { 
			    exit 1 
		        }
		}
" /proc/sys/dev/cdrom/info
