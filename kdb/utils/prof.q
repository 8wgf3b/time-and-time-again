/ nick psaris profiler


prof.events: flip `id`pid`func`time! "jjsn"$\: ()

prof.rpt:: .prof.stats prof.events

\d .prof

pid: id: 0

time: {[n; f; a]
    s: .z.p;
    id: .prof.id +: 1;
    pid: .prof.pid;
    .prof.pid: id;
    r: f . a;
    .prof.pid: pid;
    `prof.events upsert (id; pid; n; .z.p - s);
    r
    }

instr: {[n]
    m: get f: get n;
    system "d .", string first m 3;
    n set (')[.prof.time[n; f]; enlist];
    system "d .";
    n
    }

tree: {$[x ~ k: key x; x; 11h = type k; raze (.z.s ` sv x,) each k; ()]}

dirs: {(` sv x,) each key[x] except `q`Q`h`j`o`prof}

lambdas: {x where 100h = (type get @) each x}

instrall: {instr each lambdas raze tree each `., dirs `}

stats: {[e]
    e: e pj select neg sum time, nc: count i by id: pid from e;
    s: select sum time * 1e-6, n: count i, avg nc by func from e;
    s: update timepc: time % n from s;
    s: `pct xdesc update pct: 100f * time % sum time from s;
    s
    }
