timer.job: flip `name`func`time! "s*p"$\:()
timer.job ,: (`;();0Wp)


\d .timer


merge: `time xdesc upsert


add:{[t; n; f; tm]
    r:(n; f; gtime tm);
    :merge[t; $[0h > type tm; r; reverse flip r]];
    }


run:{[t; i; tm]
    j: t i;
    t: .[t; (); _; i];
    r: value (f: j `func), ltime tm;
    $[
        (-16h = type r) and not null r; :merge[t; (j `name; f; tm + r)];
        (-12h = type r) and not null r; :merge[t; (j `name; f; r)];
        :t 
        ];
    }


loop:{[t; tm]
    while[tm >= last tms:t `time; t: run[t; -1 + count tms; tm]];
    t}


until: {[d; et; f; tm] if[tm < et; @[value; f, tm; 0N!]; :d]}


.z.ts: loop `timer.job
