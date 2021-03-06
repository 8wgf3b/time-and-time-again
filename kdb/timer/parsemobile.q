/ Assuming the current directory is /kdb
tmploc: `:../temp
hdbloc: `:../data/hdb

    
reloadhdb: {
    hdb: hopen `::5012;
    neg[hdb] "\\l .";
    hclose hdb;
    }


getaumfiles: {(` sv x,) each fl where ("AUM_V4" ~ 6# string ::) each fl: key x}

savephile: {
    func: @[get;; show] last 3#"_" vs string last ` vs x;
    func x;
    }

Activity: {
    activity: `app`time xasc `app`date`time`dur xcol -4_ ("SDTN"; 1#",") 0: x;
    date: first activity `date;
    activity: (1#`date)_activity;
    .Q.dpft[hdbloc; date; `app; `activity set activity];
    @[reloadhdb; ::; `hdberror];
    }

Battery: {
    battery: `time xasc `date`time`batt`note xcol -3_ ("DTI*"; 1#",") 0: x;
    date: first battery `date;                                                 
    show battery: update note: (`$ "," vs ssr[;" ";""] ::) each note from battery;
    battery: (1#`date)_battery;
    .Q.dpt[hdbloc; date; `battery set battery];                        
    @[reloadhdb; ::; `hdberror];
    }

savephonestats: {
    fl: getaumfiles tmploc;
    savephile each fl;
    0D00:01
    }
