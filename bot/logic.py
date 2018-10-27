# bot.logic.py

import alfanous

def answer(query):
    limit = 4
    response = alfanous.do(flags={"action":"search", "query":query, "unit": "aya", "fuzzy":True, "highlight": "none", "limit": limit})
    results=[]
    if (not response["error"]["code"]):
        for i in xrange(1,  min(limit+1, response["search"]["interval"]["total"]+1)):
            result = {
                'title':  "{" + response["search"]["ayas"][i]["identifier"]["sura_arabic_name"] + " "+ str(response["search"]["ayas"][i]["identifier"]["aya_id"]) + "}",
                'body': "\n"+ response["search"]["ayas"][i]["aya"]["text"]
             }
            results.append(result)
    return results
