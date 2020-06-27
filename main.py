# -*- cod1ing:utf-8 -*-
import MeCab 
import json,config,random,re
from requests_oauthlib import OAuth1Session
import ng_word
import re

def main():
    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()

    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)

    home_url="https://api.twitter.com/1.1/statuses/home_timeline.json"
    update_url = "https://api.twitter.com/1.1/statuses/update.json"

    dame="{}、わたしがいないとだめなんですよー！"
    #yoyu="い、いえ！{}はよゆーですよ\n全然平気です！"
    watashi="わ、わたしも・・・・・・！\n{}がいないとだめだめかもしれないです・・・・・・"

    code_regex = re.compile('[1-9a-z!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]+')
    template=[dame,watashi] 

    t=MeCab.Tagger(r"-Ochasen -d /home/senk/local/mecab-dic/ipadic-utf8")
    #t=MeCab.Tagger('-Ochasen -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd') 
    t.parse("")

    res=twitter.get(home_url,params={"count":20})
    if res.status_code == 200:
        timeline=list(filter(lambda line:line["retweet_count"]==0,json.loads(res.text)))
        while True:
            tweet=timeline[random.randint(0,len(timeline)-1)]
            m = t.parseToNode((tweet["text"]))
            nouns = []
            while m:
                if m.feature.split(',')[0] == '名詞':
                    nouns.append(m.surface)
                m = m.next
            
            nouns = [nouns[i] for i in range(len(nouns)) if not code_regex.fullmatch(nouns[i])]
            if nouns==[]:
               continue
            else:
               break

        r1=random.randint(0,2)
        r2=random.randint(0,len(nouns)-1)
        tweet={"status":template[r1].format(nouns[r2])}

        res=twitter.post(update_url,params=tweet)
        if res.status_code == 200:
            print("Success!")
        else:
            print("Failed : %d"% res.status_code)

    else:
        print("Failed: %d"% res.status_code)

if __name__=='__main__':
    main()
