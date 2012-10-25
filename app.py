import web
import datetime
import sqlite3
import sys,signal
import json
import gviz_api
import redis
import tags


urls = ('/(\w*)', 'twitter','/getter/(\w*)','getter','/pietime/','piechart','/topfive/(\w*)','topFive')
cat_list = tags.cat_list
cat_dict = tags.cat_dict

render = web.template.render('templates/')
app = web.application(urls, globals())
flag = 0
update = 0
dbconn = sqlite3.connect('./tweets.db',check_same_thread=False)

keys = ['id','tweet','sname','timestamp','category','url']
r_server = redis.Redis('localhost')

def sig_int(signal,frame):
    print 'Ending brogram....'
    dbconn.commit()
    dbconn.close()
    sys.exit(0)



class homepage:
    def GET(self):
        return render.twitter()

class topFive:
    def GET(self,issue):
        ret_dict = {}
        for item in cat_dict[issue]:
            tmp = r_server.get(item)
            if tmp:
                ret_dict[item] = int(tmp)
        out = sorted(ret_dict.iteritems(),key=lambda (k,v): (v,k),reverse=True)
        acc = 0
        for el in out[:6]:
            acc = acc+ el[1]
        lst = []
        for el in out[:6]:
            lst.append([el[0],el[1],int(100*float(el[1])/float(acc) + 15)])
        return json.dumps(lst)

    def POST(self):
        return 'None'

class piechart:

    def GET(self):

        description = {'topic':('string','Topic'),
                        'tweets':('number','Tweets'),}
        data = []

        pie = {'cols':[{'id':'','label':'Topic','pattern':'','type':'string'},
                        {'id':'','label':'Tweets','pattern':'','type':'number'}],
                'rows': []}
        for key in cat_list.keys():
            pie['rows'].append({'c':[{'v':cat_list[key],'f':None},{'v':self.getNumPerCat(key),'f':None}]})
        pie['reqId'] = 0

        for key in cat_list.keys():
            data.append({'topic':cat_list[key],'tweets':self.getNumPerCat(key)})

        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        jsonz = data_table.ToJSon(columns_order=('topic','tweets'),order_by='topic',)
        return jsonz


        #return json.dumps(pie)

    def getNumPerCat(self,cat,):
        exStr = 'select count(*) from tweetz where category="%s"' % (cat,)
        dbout = dbconn.execute(exStr)
        return dbout.fetchone()[0]
                    
class getter:

    def GET(self,issue):
        lst = []
        for tweet in getCategory(issue):
            lst.append(dict(zip(keys,tweet)))

        return json.dumps(lst)

        return 'hello'


    def POST(self):
        return 'ERROR'

class twitter:


    def GET(self,issue):
        print issue
        iss_lst = issue.split()
        push_list =  {}
        return_categories = {}

        for cat in cat_list.keys():
            tweetLst = []
            if cat in iss_lst:
                return_categories[cat] = cat_list[cat]
                for tweet in getCategory(cat):
                    tweetLst.append(dict(zip(keys,tweet)))
                push_list[cat] = tweetLst




        



        return render.resp(push_list,return_categories,cat_list)



    def POST(self):
        return 'ERROR'
    
def getCategory(name,):
    exStr = 'select * from tweetz where category= "%s" order by tweet_id desc limit 6' % (name)
    dbout = dbconn.execute(exStr)
    return dbout.fetchmany(6)



if __name__ == '__main__':
    signal.signal(signal.SIGINT,sig_int)
    app.run()

