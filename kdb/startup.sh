cd ~/Documents/time-and-time-again/kdb
~/q/l32arm/q tick.q -p 5011 -g 1 -w 500
~/q/l32arm/q tick/hdb.q ../data/hdb -p 5012 -g 1 -w 1000 -T 30
~/q/l32arm/q tick/r.q localhost:5011 localhost:5012 -p 5013 -g 1 -w 500 -T 30