
"""
chat command lst 

"""

cmdlst = {"send" : ("<to> <msg>", "send message to destination"),
        "add": ("<summoner_name/id>", "add summoner to your friend list"),
        "remove": ("<summoner_name/id>", "remove summoner from your list"),
        "display": ("<type> <opt>", "display option",
            {"all": "display all your friends from list",
            "online": "display online friends from list",
            "status": "display summoner's status",
            "history": "display # of chat history associate with summoner"}
        ),
        "invite":("<summoner_name/id>", "send group chat inviation")
}

