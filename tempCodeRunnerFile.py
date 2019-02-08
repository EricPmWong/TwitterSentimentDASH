    #Tweet Cleaning 
                tweet=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+',’)", " ", tweet).split())
                blob=TextBlob(tweet.strip())

                #Sentiment Analysis
                global positive
                global negative  
                global neutral
                #global combined  
                global count
                #global total
                global text
                global positve_var
                global negative_var
                global neutral_var
                global posvar
                global negvar
                global neuvar
                global arimap 
                global ariman
                global Tx
                global Ty

                count += 1
                print("tweet pull", count)
                #Reset Sentiment to 0 for each pull
                sentiment = 0
            
                #Conducts Sentiment Analysis 

                #Reset Vars for next loop.
                

                for sen in blob.sentences:
                    
                    print(sen)
                    #Low threshold most often tweets with pictures or mentions of product are
                    #positive from a marketing perspective. Gains more traction. 
                    sentiment = sen.sentiment.polarity
                    print(sentiment)
                    if sentiment > 0.05:
                        positive += 1
                        positve_var += 1
                        print("pos")
                    #Negative tweets have a higher threshold. 
                    #Vernacular causes noises and positive tweets were False positives.(of Negatives
                    elif sentiment < -.05:
                        negative += 1
                        negative_var += 1
                        print("neg")
                    else:
                        neutral +=1
                        neutral_var += 1
                        print("neutral")

                    tokens.extend([word for word in blob.words if word not in stopwords.words('english') and word not in "RT" and word not in "’" and word not in "," and word not in "https"])
                    tokenstop = Counter(tokens)
                    Tx = [x[1] for x in tokenstop.most_common(30)]
                    Ty = [x[0] for x in tokenstop.most_common(30)]
                    #print(Tx, Ty)

            #graphs per minute
                posvar.append(positve_var)
                negvar.append(negative_var)
                neuvar.append(neutral_var)
                #Resets for next time interval to replot
                positve_var = 0
                neutral_var = 0
                negative_var = 0

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
            
                if True:
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
                #Absolute Increase
                s1.open()
                s1.write(dict(x=timex, y=timeyneg))
                s2.open()
                s2.write(dict(x=timex, y=timeyneu))
                s3.open()
                s3.write(dict(x=timex, y=timeypos))
                #Nomralized Percentages
                s4.open()
                s4.write(dict(x=timex, y=timeyneg))
                s5.open()
                s5.write(dict(x=timex, y=timeyneu))
                s6.open()
                s6.write(dict(x=timex, y=timeypos))
                #Commons Words Tokenizer
                s8.open()
                s8.write(dict(x=Tx, y=Ty))
                #Negative Posts w/Arima
                s10.open()
                s10.write(dict(x=timex, y=negvar))
                s13.open()
                s13.write(dict(x=timex, y=ariman))
                #Positive Posts w/Arima
                s12.open()
                s12.write(dict(x=timex, y=posvar))
                s14.open()
                s14.write(dict(x=timex, y=arimap))

                #s11.open()
                #s11.write(dict(x=timex, y=neuvar))
                #s9.open()
                #s9.write(dict(x=timex, y=timeysent))
                #s7.open()
                #s7.write(dict(x=, y)))


                #plt.plot(timex, timeypos, c='green')
                #plt.plot(timex, timeyneg, c='red')
                #plt.pause(.1)

                
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