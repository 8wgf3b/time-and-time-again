/q tick/r.q [host]:port[:usr:pwd] [host]:port[:usr:pwd]
/2008.09.09 .k ->.q

if[not "w"=first string .z.o;system "sleep 1"];

tbloc: hsym `$ "../data/hdb/discord/"

upd:{if[not `discord=x;:()];`discord insert y}

/ get the ticker plant and history ports, defaults are 5010,5012
.u.x:.z.x,(count .z.x)_(":5010";":5012");

/ end of day: save, clear, hdb reload
.u.end:{t:tables`.;t@:where `g=attr each t@\:`sym;.Q.hdpf[`$":",.u.x 1;tbloc;x;`sym];@[;`sym;`g#] each t;};

/ init schema and sync up from log file;cd to hdb(so client save can run)
.u.rep:{(.[;();:;].) x;if[null first y;:()];-11!y;};
/ HARDCODE \cd if other than logdir/db

/ connect to ticker plant for (schema;(logcount;log))
.u.rep .(hopen `$":",.u.x 0)"(.u.sub[`discord;`];`.u `i`L)";

