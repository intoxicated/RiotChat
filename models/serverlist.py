"""
Riot Server list
"""

#Server enum class
class Server():
    NA, BR, EUNE, EUW, KR, LAN,\
        LAS, OCE, PBE, PH, RU, TH,\
        TR, TW, VN = range(15)

#Server list
RiotServer = {
    Server.BR : ("chat.br.lol.riotgames.com", "br.api.pvp.net"),

    Server.EUNE : ("chat.eun1.riotgames.com", "eune.api.pvp.net"),

    Server.EUW : ("chat.euw1.lol.riotgames.com", "euw.api.pvp.net"),
    
    Server.KR : ("chat.kr.lol.riotgames.com", "kr.api.pvp.net"),

    Server.LAN : ("chat.la1.lol.riotgames.com", "lan.api.pvp.net"),

    Server.LAS : ("chat.la2.lol.riotgames.com", "las.api.pvp.net"),

    Server.NA : ("chat.na1.lol.riotgames.com", "na.api.pvp.net"),
 
    Server.OCE : ("chat.oc1.lol.riotgames.com", "oce.api.pvp.net"),

    Server.PBE : ("chat.pbe1.lol.riotgames.com", None),

    Server.PH : ("chatph.lol.garenanow.com", None),

    Server.RU : ("chat.ru.lol.riotgames.com", "ru.api.pvp.net"),

    Server.TH : ("chatth.lol.garenanow.com", None),
 
    Server.TR : ("chat.tr.lol.riotgames.com", "tr.api.pvp.net"),

    Server.TW : ("chattw.lol.garenanow.com", None),
 
    Server.VN : ("chatvn.lol.garenanow.com", None),
}

