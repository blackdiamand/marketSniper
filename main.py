import requests
from manifoldpy import api
import time

key = open("apikey.txt").read().strip()

wrapper = api.APIWrapper(key)

def get_answerID(market: api.Market, answerText: str):
    if market.outcomeType == "MULTIPLE_CHOICE":
        for answer in market.answers:
            if answer.get('text') == answerText:
                return answer.get('id')
def get_multi_prob(market: api.Market, answerText: str):
    if market.outcomeType == "MULTIPLE_CHOICE":
        for answer in market.answers:
            if answer.get('text') == answerText:
                return answer.get('probability')
def avg_prob(markets) -> float:
    total = 0.0
    for marketTuple in markets:
        marketFromSlug = api.get_slug(marketTuple[0])
        market = api.get_full_market(marketFromSlug.id)
        if market.outcomeType == "MULTIPLE_CHOICE":
            prob = get_multi_prob(market, marketTuple[2])
        elif market.outcomeType == "FREE_RESPONSE":
            print(marketTuple[0])
            raise Exception
        else:
            prob = market.final_probability()
        if not marketTuple[1]:
            prob = 1.0 - prob
        total += prob
    return total / len(markets)


def bet(market: api.Market, outcome: str, limitProb: float, amount: int, answerId=None):

    unixTime = time.time_ns() // 1000000
    seconds = 0
    offset = 60000
    endTime = unixTime + seconds * 1000 + offset
    print(endTime)
    betResult = wrapper.make_bet(amount=amount, contractId=market.id, outcome=outcome, limitProb=limitProb,
                                 expiresAt=endTime, answerId=answerId)

    print(betResult.text)
    print(int(time.time_ns() // 1000000))


snipe_prob = 0.19
while True:
    try:
        snipeMarketSlug = "did-an-openai-model-crack-aes192-en"
        marketFromSlug = api.get_slug(snipeMarketSlug)
        market = api.get_full_market(marketFromSlug.id)
        prob = market.final_probability()
        print(prob)
        if prob > snipe_prob:
            bet(market, "NO", 0.05, 500)

    except requests.exceptions.RequestException as e:
        pass
