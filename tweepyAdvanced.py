# NOTE: If the stream is faster than graphing it will break

#Statitstics and Visuals
import numpy as np
import pandas as pd
import time
import datetime
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

#Tweepy and Twitter Imports
from tweepy import Stream, OAuthHandler, StreamListener
from tweepy.streaming import StreamListener
import json

#tokenizer
from nltk.corpus import stopwords
#from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

#Sentiment Analysis
from textblob import TextBlob #More Acccurate
#import nltk 
import re

#Dashboard
import plotly 
import plotly.plotly as py
#import plotlywrapper as pw
#import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.tools as tls

#from statsmodels.tsa.arima_model import ARIMA
from urllib3.exceptions import ProtocolError

###########################################################
#Input brand of interest here
brand = 'gucci'
##########################################################
## SET MESSAGE NEGATIVE TWEET TOLERANCE. Graphs will not change without resets
tolerance = 10 
##########################################################

# Tokens for Twitter (removed)
API = ''
APIKEY = ''
ACC = ''
ACCKEY = ''
#Plotly Credentials
stream_ids = tls.get_credentials_file()['stream_ids']
print (stream_ids)


#Global Variables predefined
#Changing Vars
positive=0
negative=0
neutral=0
positive_var = 0
negative_var = 0
neutral_var = 0
#Persistent Vars
count = 0
timex = [] 
timeypos = [] 
timeyneg = [] 
timeyneu = [] 
timeysent = [] 
tokens=[]
tokenstop =[]
Tx=[]
Ty=[]
posvar = []
negvar = []
neuvar = []
arimap = []
ariman = []
#Text messaging condition
sms = 0


#Creating Plotly Streams
    # Absolute Senitment
stream1 = plotly.graph_objs.scatter.Stream(token =stream_ids[0])
stream2 = plotly.graph_objs.scatter.Stream(token =stream_ids[1])
stream3 = plotly.graph_objs.scatter.Stream(token =stream_ids[2])
    # Percent Sentiment
stream4 = plotly.graph_objs.scatter.Stream(token =stream_ids[3])
stream5 = plotly.graph_objs.scatter.Stream(token =stream_ids[4])
stream6 = plotly.graph_objs.scatter.Stream(token =stream_ids[5])
    # Live tweet
#stream7 = plotly.graph_objs.bar.Stream(token =stream_ids[6])
    #Word Count
stream8 = plotly.graph_objs.bar.Stream(token =stream_ids[7])
    #Heatmap 
#stream9 = plotly.graph_objs.heatmap.Stream(token =stream_ids[8])
    #Positive/Negative Rolling Mean 3
stream10 = plotly.graph_objs.scatter.Stream(token =stream_ids[9])
#stream11 = plotly.graph_objs.scatter.Stream(token =stream_ids[10])
stream12 = plotly.graph_objs.scatter.Stream(token =stream_ids[11])
stream13 = plotly.graph_objs.scatter.Stream(token =stream_ids[12])
stream14 = plotly.graph_objs.scatter.Stream(token =stream_ids[13])

# Stream objects
s1 = py.Stream(stream_ids[0])
s2 = py.Stream(stream_ids[1])
s3 = py.Stream(stream_ids[2])
s4 = py.Stream(stream_ids[3])
s5 = py.Stream(stream_ids[4])
s6 = py.Stream(stream_ids[5])
#s7 = py.Stream(stream_ids[6])
s8 = py.Stream(stream_ids[7])
#s9 = py.Stream(stream_ids[8])
s10 = py.Stream(stream_ids[9])
#s11 = py.Stream(stream_ids[10])
s12 = py.Stream(stream_ids[11])
s13 = py.Stream(stream_ids[12])
s14 = py.Stream(stream_ids[13])


#Plotly Line Graph 
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
    ],
    'annotations' : [
        dict(
            x=.05,
            y=tolerance - 1,
            xref='paper',
            yref='y',
            text='Text Warning Enabled',
            showarrow=False,
            font=dict(
                family='Courier New, monospace',
                size=16,
                color='#ffffff'
            ),
            align='center',
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='#636363',
            ax=20,
            ay=-30,
            bordercolor='#c7c7c7',
            borderwidth=2,
            borderpad=4,
            bgcolor='red',
            opacity=1
        )
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

#Toenized Word Count
trace8 = go.Bar(x= Tx, y=Ty,  stream = stream8, orientation='h')
datat = [trace8]
layoutt = go.Layout(title=(str(brand)+" Common words"))
fighist = dict(data=datat, layout=layoutt)

#Heatmap
#trace9 = go.Heatmap(x=timex, y=timeysent)
#datah = [trace9]
#layouth = go.Layout(title=(str(brand)+" Average Sentiment Indicator"))
#figheat = dict(data=datah, layout=layouth)

#Positive Tweet Moving Average
trace10 = go.Scatter(name = 'Negative', x=timex, y=negvar, mode='lines+markers', stream = stream10, text="Negative", line =dict(color ='blue', ))
trace13 = go.Scatter(name = 'Rolling Mean 3', x=timex, y=ariman, mode='lines+markers', stream = stream13, text="Predicted", line =dict(color = ('red'),
        width = 4,
        dash = 'dot'))
layout1 = go.Layout(title = (str(brand)+" Negative Tweets per minute"))
figminneg = dict(data=[trace10, trace13], layout=layout1)

#Negative Tweet Moving Average
trace12 = go.Scatter(name = 'Positive',x=timex, y=posvar, mode='lines+markers', stream = stream12,  text="Positive", line =dict(color='green'))
trace14 = go.Scatter(name = 'Rolling Mean 3', x=timex, y=arimap, mode='lines+markers', stream = stream14, text="Predicted", line =dict(color = ('red'),
        width = 4,
        dash = 'dot'))
layout2 = go.Layout(title = (str(brand)+" Positive Tweets per minute"))
figminpos = dict(data=[trace12, trace14], layout=layout2)


#########################################################################################
#Creates a class of filters, data modificaitons, etc to create twitter data
class stdOUTlistener(StreamListener):
    
#Grabbing data if not error.
    def on_data(self,data):
        
        #Sends a text message at negativity tolerance rate. See alert_sms documentation. 
        global sms
        for x in timeyneg:
            if x >= tolerance and sms == 0:
                import alert_sms
                sms += 1
    
#Try used in case of Key error
        try:
            #Set globals
            global positive
            global negative  
            global neutral
            #global combined  
            global count
            #global total
            global text
            global positive_var
            global negative_var
            global neutral_var
            global posvar
            global negvar
            global neuvar
            global arimap 
            global ariman
            global Tx
            global Ty

            

            #Count 1 per tweet pull, 1 pull can contain 2-3 tweets
            count += 1
            print("TWEET PULL", count)

            
            
            #Data Loading from json
            all_data=json.loads(data)
            tweet=all_data["text"]
            
            #Tweet Cleaning 
            tweet=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+',’)", " ", tweet).split())
            blob=TextBlob(tweet.strip())
            
            #Conducts Sentiment Analysis per tweet
            for sen in blob.sentences:
                #Create time stamps for X variables
                global initime
                t= datetime.datetime.now().strftime('%M:%S')

                print(t)
                print(sen)
                # Positive Tweet Threshold is higher. Due to many false positives
                sentiment = sen.sentiment.polarity
                print(sentiment)
                if sentiment > 0.3:
                    positive += 1
                    positive_var += 1
                    print("pos")
                #Negative tweets have a higher threshold. 
                #Vernacular causes noises and positive tweets were False positives.(of Negatives
                elif sentiment < -.01:
                    negative += 1
                    negative_var += 1
                    print("neg")
                else:
                    neutral +=1
                    neutral_var += 1
                    print("neutral")

                #Tokenizes words for graph
                tokens.extend([word for word in blob.words if word not in stopwords.words('english') and word not in "RT" and word not in "’" and word not in "," and word not in "https" and word not in str(brand) and word not in "I" and word not in "Gucci"])
                tokenstop = Counter(tokens)
                Tx = [x[1] for x in tokenstop.most_common(30)]
                Ty = [x[0] for x in tokenstop.most_common(30)]
                #print(Tx, Ty)
                s8.write(dict(x=Tx, y=Ty))


            # If TIME is not repeated, execute drawing to plotly
            if t not in timex:
                #Adds the time to X var
                timex.append(t)
                #Appending info to array for graphing
                posvar.append(positive_var)
                negvar.append(negative_var)
                neuvar.append(neutral_var)
                #Variables for ABS. and Percentage Graph
                timeypos.append(positive) 
                timeyneg.append(negative)
                timeyneu.append(neutral) 
                #totalpnn.append(total)
                #total += (positive+negative+neutral)
                # #text.append(sen)
                #combined += sen.sentiment.polarity
                #ARIMA 
                #Changed in favor of rolling mean manually calculated due to CPU overhead

                #3 day Rolling Mean calculations 
                try:
                #Calculating moving average instead
                    arimap.append(np.mean([posvar[-3],posvar[-2], posvar[-1]]))
                    ariman.append(np.mean([negvar[-3],negvar[-2], negvar[-1]]))
                    #pos
                    #modelp = ARIMA(posvar,order=(0,0,2))
                    #modelp_fit = modelp.fit(disp=0)
                    #predpos = modelp_fit.predict().astype(float)
                    #predposap = predpos[-1]
                    #arimap.append(predposap)
                    #print("Positve Arima",arimap)
                    #neg
                    #modeln = ARIMA(negvar ,order=(0,0,2))
                    ##modeln_fit = modeln.fit(disp=0)
                    #predneg = modeln_fit.predict().astype(float)
                    #prednegap = predneg[-1]
                    #ariman.append(prednegap)
                    #print("Negative Arima",ariman)
                except: 
                    arimap.append(0.00)
                    ariman.append(0.00)

                #Required Plotly channels to update graph
                s1.write(dict(x=timex, y=timeyneg))
                s2.write(dict(x=timex, y=timeyneu))
                s3.write(dict(x=timex, y=timeypos))
                #Nomralized Percentages
                s4.write(dict(x=timex, y=timeyneg))
                s5.write(dict(x=timex, y=timeyneu))
                s6.write(dict(x=timex, y=timeypos))
                #Commons Words Tokenizer
                
                #Negative Posts w/Arima
                s10.write(dict(x=timex, y=negvar))
                s13.write(dict(x=timex, y=ariman))
                #Positive Posts w/Arima
                s12.write(dict(x=timex, y=posvar))
                s14.write(dict(x=timex, y=arimap))

                #Unused Streams
                #s11.open()
                #s11.write(dict(x=timex, y=neuvar))
                #s9.open()
                #s9.write(dict(x=timex, y=timeysent))
                #s7.open()
                #s7.write(dict(x=, y)))


                #Print Indicators for testing
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
                #Reset Sentiment to 0 for each pull
                sentiment = 0
                #Resets for next time interval to replot
                positive_var = 0
                neutral_var = 0
                negative_var = 0

                print()

            #Executes same code if time stamp is same
            else:
                for sen in blob.sentences:
                    print(sen)
                    #Low threshold most often tweets with pictures or mentions of product are
                    #positive from a marketing perspective. Gains more traction. 
                    sentiment = sen.sentiment.polarity
                    print(sentiment)
                    if sentiment > 0.01:
                        positive += 1
                        positive_var += 1
                        print("pos")
                    #Negative tweets have a higher threshold. 
                    #Vernacular causes noises and positive tweets were False positives.(of Negatives
                    elif sentiment < -.01:
                        negative += 1
                        negative_var += 1
                        print("neg")
                    else:
                        neutral +=1
                        neutral_var += 1
                        print("neutral")
                
        except:
            pass
            print('error in loop')

    def on_error(self, status):
        print(status)
        pass



######################################################################################
#Loads twitter credentials
listener = stdOUTlistener()
auth = OAuthHandler(API, APIKEY)
auth.set_access_token(ACC, ACCKEY)

#Uncomment to make layout changes in plots
#py.plot(fig, filename="Twit Sent Abs")
#py.plot(figtable, filename="Live Twit Feed")
#py.plot(fighist, filename="Word Count Hist")
#py.plot(figpercent, filename="Twit Sent Percent")
#py.plot(figminneg, filename="Tweet per min neg")
#py.plot(figminpos, filename="Tweet per min pos")

#Uncomment to test Matplotlib
#plt.style.use('ggplot')
#plt.show(block=False)

s1.open()
s2.open()
s3.open()
#Nomralized Percentages
s4.open()
s5.open()
s6.open()
#Commons Words Tokenizer
s8.open()
#Negative Posts w/Arima
s10.open()
s13.open()
#Positive Posts w/Arima
s12.open()
s14.open()



#Creating Streamer, pairs authentication and listerner class
stream = Stream(auth, listener)

#Engages the stream 
while True:
    try:
        stream.filter(track=[brand], languages=["en"]);
        
    except (ProtocolError, AttributeError):
        continue
