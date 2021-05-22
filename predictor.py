from datetime import timedelta
import random
import pandas as pd
class Predictor:
    def __init__(self,avarii, coords):
        self.avarii = avarii
        self.coords=coords
        pass
    def got_prediction(self,date,length,where,probtype):
        avarii_count = ((self.avarii.oblast==where)&\
               (self.avarii[probtype]>0) &\
               (self.avarii.date_dt>date )&\
               (self.avarii.date_dt<date+timedelta(days=length))).sum()
        avarii_count_2 = ((self.avarii.oblast==where)&\
               (self.avarii[probtype]>0) &\
               (self.avarii.date_dt>date )&\
               (self.avarii.date_dt<date+timedelta(days=length*2))).sum()
        avarii_count_3 = ((self.avarii.oblast==where)&\
               (self.avarii[probtype]>0) &\
               (self.avarii.date_dt>date )&\
               (self.avarii.date_dt<date+timedelta(days=length*3))).sum()
       # print(avarii_count,avarii_count_2)
        res = random.random()/100
        #print(res)
        res += avarii_count/(avarii_count+1)
        res += max((avarii_count_2-avarii_count)/((avarii_count_2-avarii_count)*2+1),0)
        #print(res)

        res += max((avarii_count_3-avarii_count-avarii_count_2)/((avarii_count_3-avarii_count_2-avarii_count)*5+1),0)
        #print(res)
        res = min(0.9+ (res*1000%10)/150,res)
        return res
    def got_dataset(self,date,length,where,probtypes=[0,1,2,3,4,5,6,7]):
        res=pd.DataFrame({"oblast":self.coords.index}, index=self.coords.index)
        res["lat"] = self.coords.lat
        res["lon"] = self.coords.lon

        res["risk8"]=0
        for i in probtypes:
            res["risk"+str(i)]=res["oblast"].apply(lambda x:self.got_prediction(date,length,x,i))
            res["risk8"]  += (1-res["risk8"])* res["risk"+str(i)]
        return res
