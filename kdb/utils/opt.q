/ nick psaris qtips opt.q

\d .opt

config: 1#flip `opt`def`doc! "s**"$\: ()

getopt: {[c; h; x]
    p: (!). c `opt`def;
    p: .Q.def[p] .Q.opt x;
    :@[p; h; hsym]
    }

wrap: {[l; r; s] (max count each s)$ s: l,/: s,\: r}

usage: {[c;f]
    u: enlist "usage: q ", (string f), " [options]...";
    a: wrap[(7#" "), "-"; " "] string c `opt;
    a: a,' wrap["<"; "> "] c`doc;
    a: a,' wrap["("; ")"] -3!' c`def;
    u,a
    }


