#!/bin/sh

pos=0
n=0
sp="$1"
what="$2"
found=0

[ -e /proc/sys/dev/cdrom/info ] || exit 1

/bin/cat /proc/sys/dev/cdrom/info | {
	IFS=":"
	while read name val; do
	    name=$(echo "$name" | xargs)
	    val=$(echo "$val" | xargs)
	    newname="${name%%${what}}"
	    [ "$name" = "drive name" -a "$val" = "$sp" ] && found=1
	    [ "$found" -eq 1 -a "$val" = "1" -a "$name" != "$newname" ] && exit 0
	done
	exit 1
}
