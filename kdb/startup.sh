cd ~/Documents/time-and-time-again/kdb
~/q/l32arm/q tick.q discord ../data/tplogs -p 5011 -g 1 -w 500 < /dev/null > ~/Documents/log1 2>&1&
~/q/l32arm/q tick/hdb.q ../data/hdb -p 5012 -g 1 -w 1000 -T 30 < /dev/null > ~/Documents/log2 2>&1&
~/q/l32arm/q tick/disr.q localhost:5011 localhost:5012 -p 5013 -g 1 -w 500 -T 30 < /dev/null > ~/Documents/log3 2>&1&
~/q/l32arm/q cep.q -t 100 -p 5030 -g 1 -w 1000 -T 30 < /dev/null > ~/Documents/cep 2>&1&
~/q/l32arm/q tick/traffic.q -p 5020 -g 1 -w 100 -T 30 < /dev/null > ~/Documents/traffic 2>&1&
~/q/l32arm/q tick/disclient.q -p 5015 -g 1 -w 100 -T 30 -s 2 -b< /dev/null > ~/Documents/dclient 2>&1&
