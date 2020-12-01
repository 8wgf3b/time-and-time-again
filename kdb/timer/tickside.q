\l timer/helper.q

eodDiscord: {
    h: hopen `::5013;
    0N!h (`eod; .z.d);
    hclose h;
    dailyonce 0D18:30
    }
