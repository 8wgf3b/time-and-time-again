\l timer/helper.q

eodDiscord: {[tm]
    h: hopen `::5013;
    0N!h (`eod; .z.d);
    hclose h;
    dailyonce 0D18:30
    }

tickside.jobs: enlist (`eoddiscord; eodDiscord; dailyonce 0D18:30);

