discord: flip `time`sym`date`channel`message! "nsds*"$\: ();

upd: insert;

helper:{$[(type x) or not count x; 1; t: type first x; all t = type each x; 0]};

checker: {select from (raze {([]table:enlist x;columns:enlist where not helper each flip .Q.en[`:.]`. x)} each tables[]) where 0<count each columns}

dislogs: hsym `$ "../data/tplogs/discord", string @;

saver: {
    -11! dislogs x;
    update message: enlist each message from `discord where -10 = type each message;
    .Q.hdpf[`::5012; `:../data/hdb; x; `time]
    }

