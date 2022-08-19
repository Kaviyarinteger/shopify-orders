#!/usr/bin/env python
# coding: utf-8

# In[3]:


#pip --version


# In[ ]:


# Required Packages and Modules here
import pandas as pd 
import requests 
import json
import schedule
import time
from datetime import datetime  
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import gspread_dataframe as gd

# Scope of the sheets
# Adding the Credentials which is coming from google cloud -> service account -> json file(credentials.json) 
# Autorizing the sheet with the help of credentials(creds)
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials4.json", scope)
client = gspread.authorize(creds)

# Setting the timer here based on your requirement
def timer():
    schedule.every(10).seconds.do(orders)
    #schedule.every(1).minutes.do(func1)
    while 1:
        schedule.run_pending()
        time.sleep(1)
# Header method(Orders) 

try:  
    def orders():
    
# Creating empty list for append the records        
        lst=[]
# Using sheets method for importing the records in the g-sheet
        def sheets(df):
            ws = client.open("fbb3").worksheet("Sheet3")
            existing = pd.DataFrame(ws.get_all_records())
            updated = existing.append(df)
            print("Current time",datetime.now())
            gd.set_with_dataframe(ws,updated)
# Removing unwanted records here    
        def removing_rows(df1):
            index_names=df1[df1['created_at'] == 0 ].index
            df1.drop(index_names, inplace = True)
            lst.append(df1)
            sheets(pd.concat(lst))
# Getting the response(Order data) using the requests 
        def responses():   
            response_1=requests.get("https://53c61a91b322fdd064867f4a3d0f1ea0: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@9shine.myshopify.com/admin/api/2022-07/orders.json?limit=250&status=any")
            response_2=json.loads(response_1.text)
            df1=pd.DataFrame(response_2["orders"])
            return df1
# Handling the dates here
        df1=responses()
        for i in range(0,len(df1['created_at'])):
            time=datetime.fromisoformat(str(df1['created_at'][i]))
            time2=datetime.now()
            time2=time2.date()
            if str(time)<=str(datetime.now()) and str(time)>=str(time2)+str(' 00:00:00+00:00'):
                df1['created_at'][i]=time2
            else:
                df1['created_at'][i]=0
# calling removing_rows functon which located inside timer function
        removing_rows(df1)
# Calling timer function
    timer()
except Exception as e:
    print(e)
    print("ERROR DETECTED")

#def main():
    #timer
    
#if __name__ == "__main__":
    #main()


# In[ ]:




