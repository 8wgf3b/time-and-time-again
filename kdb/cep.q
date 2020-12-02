/ nick psaris cep

\l utils/log.q
\l utils/opt.q
\l utils/prof.q
\l timer/timer.q
\l timer/tickside.q


c: .opt.config
c,: (`lloc; `:../logs/timer; "log files folder loc")
c,: (`llvl; 2; "log level")
c,: (`debug; 0b; "dont start engine")

newhdl: {[folder;tm] .log.h: neg hopen ` sv folder, `$ string `date$tm; dailyonce 0D00}

main: {[p]
    .timer.add[`timer.job] .' tickside.jobs;
    .timer.add[`timer.job; `newlog; newhdl[p`lloc];.z.p]
    }

p: .opt.getopt[c; `lloc] .z.x
if[`help in key p; -1 .opt.usage[1_c; .z.f]; exit 1]
.log.lvl: p `llvl
newhdl[p`lloc; .z.p];
if[not p `debug; main[p]]
.log.inf "Started CEP Engine :)"
