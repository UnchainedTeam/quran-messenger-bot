# bot.logic.py

import alfanous

def answer(query):
    limit = 3
    response = alfanous.do(flags={"action":"search", "query":query, "unit": "aya", "fuzzy":True, "highlight": "none", "limit": limit})
    print query.encode('utf-8')
    print response["error"]
    reply=""
    if (not response["error"]["code"]):
        for i in xrange(1,  min(limit+1, response["search"]["interval"]["total"]+1)):
             reply += "{" + response["search"]["ayas"][i]["identifier"]["sura_arabic_name"] + " "+ str(response["search"]["ayas"][i]["identifier"]["aya_id"]) + "}"
             reply += "\n"+ response["search"]["ayas"][i]["aya"]["text"]
             reply += "\n\n"
    return reply
