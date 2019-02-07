# NOTE: If the stream is faster than graphing it will break

#Alerts

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
import nltk 
import re

#Twilio text msging

#tokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

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

#Arima

from statsmodels.tsa.arima_model import ARIMA


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

## SET MESSAGE NEGATIVE TWEET TOLERANCE
tolerance = 10 

count = 0
positive=0
negative=0
neutral=0
combined=0
total =0
positve_var = 0
negative_var = 0
neutral_var = 0


timex = [] #X var
timeypos = [] #Green Var
timeyneg = [] #Red Var
timeyneu = [] # Blue var
timeysent = [] # Dashed line
totalpnn = [] 
#texty = []
#textx = []
# Plotly stuff
tokens=[]
posvar = []
negvar = []
neuvar = []

#Arima
arimap = []
ariman = []

#Alert Condition
#Change to 1 to shut off alerts
sms = 0


stream_ids = tls.get_credentials_file()['stream_ids']
print (stream_ids)

#Count Vectorizer





#Creating Plotly Streams
# Absolute Senitment
stream1 = plotly.graph_objs.scatter.Stream(token =stream_ids[0], maxpoints=60)
stream2 = plotly.graph_objs.scatter.Stream(token =stream_ids[1], maxpoints=60)
stream3 = plotly.graph_objs.scatter.Stream(token =stream_ids[2], maxpoints=60)
# Percent Sentiment
stream4 = plotly.graph_objs.scatter.Stream(token =stream_ids[3], maxpoints=60)
stream5 = plotly.graph_objs.scatter.Stream(token =stream_ids[4], maxpoints=60)
stream6 = plotly.graph_objs.scatter.Stream(token =stream_ids[5], maxpoints=60)
# Live tweet
#stream7 = plotly.graph_objs.bar.Stream(token =stream_ids[6], maxpoints=60)
#Count Vectorizer
stream8 = plotly.graph_objs.histogram.Stream(token =stream_ids[7], maxpoints=60)
#Heatmap 
#stream9 = plotly.graph_objs.heatmap.Stream(token =stream_ids[8], maxpoints=60)
stream10 = plotly.graph_objs.scatter.Stream(token =stream_ids[9], maxpoints=60)
#stream11 = plotly.graph_objs.scatter.Stream(token =stream_ids[10], maxpoints=60)
stream12 = plotly.graph_objs.scatter.Stream(token =stream_ids[11], maxpoints=60)
stream13 = plotly.graph_objs.scatter.Stream(token =stream_ids[12], maxpoints=60)
stream14 = plotly.graph_objs.scatter.Stream(token =stream_ids[13], maxpoints=60)


# Stream objects
s1 = py.Stream(stream_ids[0])
s2 = py.Stream(stream_ids[1])
s3 = py.Stream(stream_ids[2])
s4 = py.Stream(stream_ids[3])
s5 = py.Stream(stream_ids[4])
s6 = py.Stream(stream_ids[5])
s7 = py.Stream(stream_ids[6])
s8 = py.Stream(stream_ids[7])
#s9 = py.Stream(stream_ids[8])
s10 = py.Stream(stream_ids[9])
#s11 = py.Stream(stream_ids[10])
s12 = py.Stream(stream_ids[11])
s13 = py.Stream(stream_ids[12])
s14 = py.Stream(stream_ids[13])



#title=(str(brand)+" Sentiment Analysis")
#Line Graph 
trace1 = go.Scatter(name = 'Negative', x=timex, y=timeyneg, mode='lines+markers', stream = stream1, fill = 'tozeroy',  stackgroup='one', text="Negative",)
trace2 = go.Scatter(name = 'Neutral', x=timex, y=timeyneu, mode='lines+markers', stream = stream2, fill = 'tonexty',   stackgroup='one', text="Neutral",)
trace3 = go.Scatter(name = 'Positive',x=timex, y=timeypos, mode='lines+markers', stream = stream3, fill = 'tonexty',   stackgroup='one', text="Positive",)
data = [trace1, trace2, trace3]
layout = {'title':(str(brand)+" Sentiment Analysis"),
'shapes': [
{'type': 'line',
'xref': 'paper',
'x0': 0,
'y0': tolerance,
'x1': 1, #datetime.datetime.now().strftime('%M:%S'),
'y1': tolerance,
'line': {
'color': 'red',
'width': 4,
'dash': 'dashdot'}}
    ]
}

fig = dict(data=data, layout=layout)

#Line Graph Percentage
trace4 = go.Scatter(name = 'Negative percent', x=timex, y=timeyneg, mode='lines+markers', stream = stream4, fill = 'tozeroy',  stackgroup='one', text="Negative", groupnorm='percent',  )
trace5 = go.Scatter(name = 'Neutral percent', x=timex, y=timeyneu, mode='lines+markers', stream = stream5, fill = 'tonexty',   stackgroup='one', text="Neutral",)
trace6 = go.Scatter(name = 'Positive percent',x=timex, y=timeypos, mode='lines+markers', stream = stream6, fill = 'tonexty',   stackgroup='one', text="Positive",)
datap = [trace4, trace5, trace6]
layoutp = go.Layout(title=(str(brand)+" Sentiment Analysis Normalized"))
figpercent = dict(data=datap, layout=layoutp)

#Tweet Display Disabled 
#trace7 = go.Table(stream=stream7, header = dict(values=['Tweets']),
    #cells = dict(values=[texty]))
#dataf = [trace7]
#layoutt = go.Layout(title=(str(brand)+" Live Tweets"))
#figtable = dict(data=dataf, layout=layoutt)

#Tokenize Word Count
trace8 = go.Histogram(y=tokens, stream = stream8)
datat = [trace8]
layoutt = go.Layout(title=(str(brand)+" Common words"))
fighist = dict(data=datat, layout=layoutt)

#Heatmap
#trace9 = go.Heatmap(x=timex, y=timeysent)
#datah = [trace9]
#layouth = go.Layout(title=(str(brand)+" Average Sentiment Indicator"))
#figheat = dict(data=datah, layout=layouth)

#Tweet per interval

#Positive Track
trace10 = go.Scatter(name = 'Negative', x=timex, y=negvar, mode='lines+markers', stream = stream10, text="Negative", line =dict(color ='blue'))
trace13 = go.Scatter(name = 'Predicted', x=timex, y=ariman, mode='lines+markers', stream = stream13, text="Predicted", line =dict(color ='orange'))
layout1 = go.Layout(title = (str(brand)+" Negative Tweets per minute"))
figminneg = dict(data=[trace10, trace13], layout=layout1)

#Negative Track
trace12 = go.Scatter(name = 'Positive',x=timex, y=posvar, mode='lines+markers', stream = stream12,  text="Positive", line =dict(color='green'))
trace14 = go.Scatter(name = 'Predicted', x=timex, y=arimap, mode='lines+markers', stream = stream14, text="Predicted", line =dict(color ='orange'))
layout2 = go.Layout(title = (str(brand)+" Positive Tweets per minute"))
figminpos = dict(data=[trace12, trace14], layout=layout2)





#Creates a class of filters, data modificaitons, etc to create twitter data

class stdOUTlistener(StreamListener):
    
    
#Grabbing Data
    def on_data(self,data):
        
        global sms
        for x in timeyneg:
            if x >= tolerance and sms == 0:
                import alert_sms
                sms += 1
    
#Try used in case of Key error
        try:

            global initime
            t= datetime.datetime.now().strftime('%M:%S')
            
            #Data Loading
            all_data=json.loads(data)
            tweet=all_data["text"]
            
            #Tweet Cleaning 
            tweet=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+',’)", " ", tweet).split())
            blob=TextBlob(tweet.strip())

            #Sentiment Analysis
            global positive
            global negative  
            global neutral
            global combined  
            global count
            global total
            global text
            global positve_var
            global negative_var
            global neutral_var
            global posvar
            global negvar
            global neuvar
            global arimap 
            global ariman


            count += 1
            sentiment = 0
        
            # Conducts Sentiment Analysis 
            
            for sen in blob.sentences:
                sentiment = sentiment+ sen.sentiment.polarity
                
                #Low threshold most often tweets with pictures or mentions of product are
                #positive from a marketing perspective. Gains more traction. 
    
                if sentiment > 0.1:
                    positive += 1
                    positve_var += 1

                #Negative tweets have a higher threshold. 
                #Vernacular causes noises and positive tweets were False positives.(of Negatives)
                
                elif sentiment < -.1:
                    negative += 1
                    negative_var += 1
                else:
                    neutral +=1
                    neutral_var += 1
            
                #text.append(sen)
                combined += sen.sentiment.polarity
                total += (positive+negative+neutral)
                
                # Tokenizer
                tokens.extend([word for word in blob.words if word not in stopwords.words('english') and word not in "RT" and word not in "’" and word not in ","])
                print(count)
                
                
            #ARIMA 
            #Change p and q according to assumptions
            
            if len(timex) > 5:
                try:
                    #pos
                    modelp = ARIMA(posvar,order=(0,0,1))
                    modelp_fit = modelp.fit(disp=0)
                    predpos = modelp_fit.predict().astype(float)
                    predposap = predpos[-1]
                    arimap.append(predposap)
                    #print("Positve Arima",arimap)
                    #neg
                    modeln = ARIMA(negvar ,order=(0,0,1))
                    modeln_fit = modeln.fit(disp=0)
                    predneg = modeln_fit.predict().astype(float)
                    prednegap = predneg[-1]
                    ariman.append(prednegap)
                    #print("Negative Arima",ariman)
                except:
                    arimap.append(0)
                    ariman.append(0)
            else: 
                arimap.append(0)
                ariman.append(0)
               


                #modeln = ARIMA(negvar[0:-1], order(0,0,1))


            

            #Creates a list used for plotting
            timex.append(t)
            timeypos.append(positive + negative + neutral) 
            timeyneg.append(negative)
            timeyneu.append(neutral+negative) 
            timeysent.append(combined) 
            totalpnn.append(total)
            
            #graph vars
            posvar.append(positve_var)
            negvar.append(negative_var)
            neuvar.append(neutral_var)
           
        

            s1.open()
            s1.write(dict(x=timex, y=timeyneg))
            s2.open()
            s2.write(dict(x=timex, y=timeyneu))
            s3.open()
            s3.write(dict(x=timex, y=timeypos))
            s4.open()
            s4.write(dict(x=timex, y=timeyneg))
            s5.open()
            s5.write(dict(x=timex, y=timeypos))
            s6.open()
            s6.write(dict(x=timex, y=timeyneu))
            #s7.open()
            #s7.write(dict(x=, y)))
            s8.open()
            s8.write(dict(y=tokens))
            #s9.open()
            #s9.write(dict(x=timex, y=timeysent))
            s10.open()
            s10.write(dict(x=timex, y=negvar))
            #s11.open()
            #s11.write(dict(x=timex, y=neuvar))
            s12.open()
            s12.write(dict(x=timex, y=posvar))

            s13.open()
            s13.write(dict(x=timex, y=ariman))
            s14.open()
            s14.write(dict(x=timex, y=arimap))


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
            #print(total)
            #print(totalpnn)

            #Resets vars
            positve_var = 0
            neutral_var = 0
            negative_var = 0

        except:
            pass
    def on_error(self, status):
        print(status)
        pass

listener = stdOUTlistener()

#Loads twitter credentials
auth = OAuthHandler(API, APIKEY)
auth.set_access_token(ACC, ACCKEY)




#py.plot(fig, filename="Twit Sent Abs")

#py.plot(figtable, filename="Live Twit Feed")

#py.plot(fighist, filename="Word Count Hist")

#py.plot(figpercent, filename="Twit Sent Percent")

#py.plot(figminneg, filename="Tweet per min neg")
#py.plot(figminpos, filename="Tweet per min pos")


#Uncomment to test Matplotlib
#plt.style.use('ggplot')
#plt.show(block=False)


#Creating Streamer, pairs authentication and listerner class
stream = Stream(auth, listener)
stream.filter(track=[brand], languages=["en"]);

