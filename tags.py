economy = ['economy','taxes','tax','unemployment','jobs','job','fiscal policy','fiscal','economic','economy','banking','finance','financial','spending','raise tax', 'stimulus','wall street','recovery','employment','recession','business','small business']
health_care = ['health','health care', 'health', 'deathpanel','health care act','affordable health','health reform','doctor','patients','hospital','medicare','medicaid','insurance','premium','malpractice',]
foreign_policy = ['fpolicy','foreign policy','military','force','terrorist','attack','war','afghanistan','iraq','iran','korea','libya','war on terror','israel','defense','defense department','overseas','negotiation','nations','withdraw','coalition','dictator','muslim','commander','threat','radical','islam','middle east','region',]
#derrick_rose = ['drose','derrick rose','bulls','basketball','chicago']

super_tuesday = ['supertuesday','super tuesday','super tuesday','#supertuesday','primary','primaries','alaska','georgia','idaho','massachusetts','north dakota','ohio','oklahoma','tennessee','vermont','virginia',]
#mass = ['mass','massachusetts','ma','boston',

tweet_search = 'election,vote,Santorum,Romney,Ron Paul,Gingrich,Obama,basketball,derrick rose,nba,chicago bulls'

category_list = [economy,health_care,foreign_policy,super_tuesday,]

cat_dict = {}
for el in category_list:
    cat_dict[el[0]] = el

cat_list = {'economy':'Economy','health':'Health Care','fpolicy':'Foreign Policy',
        'abortion':'Abortion','immigration':'Immigration','supertuesday': 'Super Tuesday',}
#cat_dict = {'fpolicy':foreign_policy,'health':health_care,'economy':economy,}


candidates = [3,'santorum','romney,','paul','gingrich','obama']
parties = [3,'democrat','republican','gop','right','left','green','libertarian','tea']
voting = [2,'2012','ballot','vote','voting','voted','votes','delegates','caucus','candidates','primaries','super','tuesday','win','victory',]
issues = [2,'economy','jobs','drilling','bailout','health','care','reform','tax','obamacare','welfare','muslim','abortion','drugs','energy','iraq','afghanistan','war','budget']
#drose = [3,'trade','basketball','nba','derrick','rose','chicago','bulls']
set_list = [candidates,parties,voting,issues,]

