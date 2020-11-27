/ nick psaris log.q

\d .log

h: -2
lvl: 2
unit: "BKMGTP"
mult: 5 (1024*)\ 1

mem: {@[string "i"$ (3#x) % mult m; 2; ,; unit m: mult bin x 2]}

hdr: {string[(.z.d; .z.t)], mem system "w"}

msg: {if[x <= lvl; h " " sv hdr[], (y; $[10h = type z; z; -3!z])]}


err: msg[0; "[E]"]
wrn: msg[0; "[W]"]
inf: msg[0; "[I]"]
dbg: msg[0; "[D]"]
trc: msg[0; "[T]"]
