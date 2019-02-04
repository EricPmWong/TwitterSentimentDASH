#Statitstics and Visuals
import numpy as np
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#Tweepy
from tweepy import Stream, OAuthHandler, StreamListener
from tweepy.streaming import StreamListener
import json

#Sentiment Analysis
from textblob import TextBlob #More Acccurate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #Faster
import re


#Dashboard
import plotly 
import plotly.plotly as py
import plotlywrapper as pw
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.tools as tls

###########################################################
#Input brand of interest here
brand = 'Gucci'
##########################################################


# Tokens for Twitter
API = 'sFb8T5BX4PAc50iCj1RMnty8m'
APIKEY = 'b4Eawn17wX2cf2sjBAmkEn8RFlQFezhdakIRcl8mbJKlkqjiZ1'
ACC = '1087768519268282370-TK5Gp6EfuFTj4WlLVhNRujzVjzOlgY'
ACCKEY = 'nC5z5yiLweU17qDtrdwrsQmtAJiLUb2915c2IHGAkngYS'



#Creates time as a function seconds.

#def calctime(x):
    #return time.time() - x

#Plotting variables

count = 0
positive=0
negative=0
neutral=0
combined=0

timex = [] #X var
timeypos = [] #Green Var
timeyneg = [] #Red Var
timeyneu = [] # Blue var
timeysent = [] # Dashed line

# Plotly stuff

stream_ids = tls.get_credentials_file()['stream_ids']
print (stream_ids)



stream1 = plotly.graph_objs.scatter.Stream(token =stream_ids[0], maxpoints=60)
stream2 = plotly.graph_objs.scatter.Stream(token =stream_ids[1], maxpoints=60)
stream3 = plotly.graph_objs.scatter.Stream(token =stream_ids[2], maxpoints=60)
stream4 = plotly.graph_objs.scatter.Stream(token =stream_ids[3], maxpoints=60)
stream5 = plotly.graph_objs.scatter.Stream(token =stream_ids[4], maxpoints=60)
stream6 = plotly.graph_objs.scatter.Stream(token =stream_ids[5], maxpoints=60)
stream7 = plotly.graph_objs.scatter.Stream(token =stream_ids[6], maxpoints=60)

s1 = py.Stream(stream_ids[0])
s2 = py.Stream(stream_ids[1])
s3 = py.Stream(stream_ids[2])


trace1 = go.Scatter(name = 'Neagtive', x=timex, y=timeyneg, mode='lines+markers', stream = stream1, fill = 'tozeroy',  stackgroup='one', text="Negative",)
trace2 = go.Scatter(name = 'Neutral', x=timex, y=timeyneu, mode='lines+markers', stream = stream2, fill = 'tonexty',   stackgroup='one', text="Neutral",)
trace3 = go.Scatter(name = 'Positive',x=timex, y=timeypos, mode='lines+markers', stream = stream3, fill = 'tonexty',   stackgroup='one', text="Positive",)

data = [trace1, trace2, trace3]

#Scrolling layout
movingscroll = list(timex[-10:-1])

#
layout = go.Layout(title=(str(brand)+" Sentiment Analysis"))

fig = dict(data=data, layout=layout)

#Creates a class of filters, data modificaitons, etc to create twitter data

class stdOUTlistener(StreamListener):
    
    
#Grabbing Data
    def on_data(self,data):
        
    
#Try used in case of Key error
        try:
            
        
            #Time setting of tweet
            global initime
            t= datetime.datetime.now().strftime('%M:%S')
            
            #Data Loading
            all_data=json.loads(data)
            tweet=all_data["text"]
            
            #Tweet Cleaning 
            tweet=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
            blob=TextBlob(tweet.strip())

            #Sentiment Analysis
            global positive
            global negative  
            global neutral
            global combined  
            global count
            
            count += 1
            sentiment = 0
        
            # Conducts Sentiment Analysis 
            
            for sen in blob.sentences:
                sentiment = sentiment+ sen.sentiment.polarity
                
                #Low threshold most often tweets with pictures or mentions of product are
                #positive from a marketing perspective. Gains more traction. 
    
                if sentiment > 0.1:
                    positive += 1
                    
                #Negative tweets have a higher threshold. 
                #Vernacular causes noises and positive tweets were False positives.(of Negatives)
                
                elif sentiment < -.1:
                    negative += 1
                    
                else:
                    neutral +=1
                
                
                combined += sen.sentiment.polarity
                
            
            
            #Creates a list used for plotting
            timex.append(t)
            timeypos.append(positive + negative + neutral) 
            timeyneg.append(negative)
            timeyneu.append(neutral+negative) 
            timeysent.append(combined) 
            
            s1.open()
            s1.write(dict(x=timex, y=timeyneg))
            
            s2.open()
            s2.write(dict(x=timex, y=timeyneu))

            s3.open()
            s3.write(dict(x=timex, y=timeypos))

            


            #plt.plot(timex, timeypos, c='green')
            #plt.plot(timex, timeyneg, c='red')
            #plt.pause(.1)

            #print("tweet num", count)
            #print("time", t)
            #print(blob)
            #print("LABELED AS ", sen.sentiment.polarity)
            #print("pos", positive)
            #print("negs", negative)
            #print("neutral", neutral)
            #print("combined sent", compound)
            #print(sentiment)
            

            
        except:
            pass
    def on_error(self, status):
        print(status)
        pass

listener = stdOUTlistener()

#Loads twitter credentials
auth = OAuthHandler(API, APIKEY)
auth.set_access_token(ACC, ACCKEY)



py.plot(fig)
#Uncomment to test Matplotlib
#plt.style.use('ggplot')
#plt.show(block=False)


#Creating Streamer, pairs authentication and listerner class
stream = Stream(auth, listener)
stream.filter(track=[brand], languages=["en"]);

