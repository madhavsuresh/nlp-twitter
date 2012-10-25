import pycurl, json 
import urllib
import sqlite3
import sys
import signal
import redis
import tags
import time

set_list = tags.set_list
category_list = tags.category_list


STREAM_URL = 'https://stream.twitter.com/1/statuses/filter.json'
dbconn = sqlite3.connect('./tweets.db',check_same_thread=False)
cur = dbconn.cursor()
dbconn.isolation_level = None
r_server = redis.Redis('localhost')

def sig_int(signal,frame):
    print 'Ending brogram....'
    dbconn.commit()
    dbconn.close()
    sys.exit(0)


def attach_nozzle(callback,args):
    conn = pycurl.Curl()
    conn.setopt(pycurl.USERPWD,'madman92:madman18')
    conn.setopt(pycurl.URL,STREAM_URL)
    conn.setopt(pycurl.WRITEFUNCTION,callback)

    data = urllib.urlencode(args)
    conn.setopt(pycurl.POSTFIELDS,data)

    conn.perform()


def hose(data):
    score = 0
    bonus = 0

    tweet_dict =  json.loads(data)#['text'].lower()
    if 'text' in tweet_dict:
        tweet = tweet_dict['text'].lower()
        time_stamp = ''
        geo = ''
        screen_name = ''
        url = ''
        sanitized = tweet.split()


        if 'created_at' in tweet_dict:
            time_stamp = tweet_dict['created_at']

        if 'geo' in tweet_dict:
            geo  = tweet_dict['geo']
        if 'screen_name' in tweet_dict['user']:
            screen_name = tweet_dict['user']['screen_name']
        if len(tweet_dict['entities']['urls']) > 0:
            url =  tweet_dict['entities']['urls']
            url = url[0]['expanded_url']

        for s in set_list:
            tmp = scoreFromSet(sanitized,s)
            if tmp > 0:
                bonus = bonus + 1
            score = score + tmp
        score = score + bonus

        if score > 5:
            category = [0,'']
            for c in category_list:
                tmp =  categorizeTweet(tweet,c[1:])
                if tmp > category[0]:
                    category = (tmp,c[0])
                    print category
            lst = (tweet,screen_name,time_stamp,category[1],url,)
            #jprint category
            #$print category[1]
            cur.execute('INSERT into tweetz (tweet,sname,timestamp,category,linkz) VALUES (?,?,?,?,?)',lst)

def categorizeTweet(tweet,category):

    score = 0
    for element in category:
        if element in tweet:
            score  = score + 1
            r_server.incr(element)
    return score


def getNumPerCat(self,cat,):
    exStr = 'select count(*) from tweetz where category="%s"' % (cat,)
    dbout = dbconn.execute(exStr)
    return dbout.fetchone()[0]


def scoreFromSet(tweet,set_name):
    match = list(set(tweet) & set(set_name[1:]))
    return set_name[0] * len(match)


if __name__== '__main__':
    signal.signal(signal.SIGINT,sig_int)
    args = { 'track':tags.tweet_search
            }
    attach_nozzle(hose,args,)
#    f = open('./tweetz.out','r')
#    for line in f:
#        if line != '\n':
#            #time.sleep(2)
            #hose(line)



