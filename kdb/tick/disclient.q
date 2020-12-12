.z.ws:{neg[.z.w].j.j @[value value @;x;{`$ "'",x}];}

rdb: hopen `::5013
hdb: hopen `::5012

nsa: {(count; sum count each; avg count each) @\: x}

dailyuser: {
    yesterday: -1 + `date$ .z.p + 0D05:30;
    c: ((=;`date;yesterday); (=; `sym; 1#x));
    b: `time`channel`message! `time`channel`message;
    d: hdb ({?[`discord; x; 0b; y]}; c; b);
    astats: exec nsa message from d;
    cstats: exec nsa message by channel from d;
    tstats: 0^(til 24)#exec nsa message by 1 xbar `hh$time from d;
    (astats; cstats; tstats)
    }
