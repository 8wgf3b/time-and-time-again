cd ~/Documents/time-and-time-again/kdb
~/q/l32arm/q tick.q sym ../data/tplogs -p 5011 -g 1 -w 500 < /dev/null > ~/Documents/log1 2>&1&
~/q/l32arm/q tick/hdb.q ../data/hdb -p 5012 -g 1 -w 1000 -T 30 < /dev/null > ~/Documents/log2 2>&1&
~/q/l32arm/q tick/r.q localhost:5011 localhost:5012 -p 5013 -g 1 -w 500 -T 30 < /dev/null > ~/Documents/log3 2>&1&

