.u.rep:{(.[;();:;].) x; };

upd:{
    if[not `discord=x;:()];
    `discord insert y;
    delete from `discord where time < .z.p + 0D05:20;
    `CST set `messages xdesc select messages: count message by channel, sym from `discord;
    `CT set `messages xdesc select messages: count message by channel from `discord;
    `ST set `messages xdesc select messages: count message by sym from `discord;
    }

.u.rep @ (hopen `::5011)".u.sub[`discord;`]";
