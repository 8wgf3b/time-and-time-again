/q tick/r.q [host]:port[:usr:pwd] [host]:port[:usr:pwd]
/2008.09.09 .k ->.q

if[not "w"=first string .z.o;system "sleep 1"];

tbloc: hsym `$ "../data/hdb/discord/"

upd:{if[not `discord=x;:()];`discord insert y}

offdt: {`date$y + x}[D05:30] 

fill: {
    -11! ` sv `:../data/tplogs, `$ "discord", string x;
    delete from `discord where date <> offdt .z.p;
    `time xasc `discord;
    }

/ get the ticker plant and history ports, defaults are 5010,5012
.u.x:.z.x,(count .z.x)_(":5010";":5012");

/ end of day: save, clear, hdb reload
.u.end:{};
eod: {.Q.hdpf[`::5012; `:../data/hdb/; x; `time]}

/ init schema and sync up from log file;cd to hdb(so client save can run)
.u.rep:{(.[;();:;].) x; @[fill;;::] @/: offdt[.z.p] - til 2};
/ HARDCODE \cd if other than logdir/db

/ connect to ticker plant for (schema;(logcount;log))
.u.rep @ (hopen `$":",.u.x 0)".u.sub[`discord;`]";

