/ nick psaris cep

\l utils/log.q
\l utils/opt.q
\l utils/prof.q
\l timer/timer.q
\l timer/tickside.q
\l timer/parsemobile.q

c: .opt.config
c,: (`t; 100; "set timer")
c,: (`lloc; `:../logs/timer; "log files folder loc")
c,: (`llvl; 2; "log level")
c,: (`debug; 0b; "dont start engine")

newhdl: {[folder;tm]    
    .log.h: neg hopen loc:` sv folder, `$ string `date$tm;
    .log.inf "new log file location: ", -3!loc;
    dailyonce 0D00
    }

main: {[p]
    .timer.add[`timer.job; `newlog; newhdl[p`lloc]; dailyonce 0D00:00]
    .timer.add[`timer.job] . (`phonestats; savephonestats; .z.p);
    }

p: .opt.getopt[c; `lloc] .z.x
if[`help in key p; -1 .opt.usage[1_c; .z.f]; exit 1]
.log.lvl: p `llvl
newhdl[p`lloc; .z.p];
if[any `t = key p; system "t 100"]
if[not p `debug; main[p]]
.log.inf "Started CEP Engine :)"
