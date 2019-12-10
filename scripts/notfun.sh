#!/bin/sh

for f in *.pcap; do
  d="$(cat $f | grep file | cut -c 3-)"
  mv "$f" "$d"
  sed -i '$d' "$d"
  sed -i '/^$/d' "$d"
done

i=1
while [ $i -lt 100 ]
do
  if [ $i -lt 10 ]; then
    mv "file$i" "file00$i"
  else
    mv "file$i" "file0$i"
  fi
  i=$((i+1))
done

cat "file*" > main.c
