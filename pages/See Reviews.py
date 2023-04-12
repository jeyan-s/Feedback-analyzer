import base64
import sqlite3
import os
import streamlit as st 
from collections import defaultdict
import pandas as pd

#setting up the expert.ai environment variables with the credentials
os.environ["EAI_USERNAME"] = 'jeyannino001@gmail.com'
os.environ["EAI_PASSWORD"] = 'Nino@001'
from expertai.nlapi.cloud.client import ExpertAiClient
client = ExpertAiClient()

st.set_page_config(page_title='See Reviews', page_icon='', layout="wide", initial_sidebar_state="collapsed", menu_items=None)

#adding background to the web page 
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def getConnection():
    sqliteConnection = sqlite3.connect('feedbacks.db')
    return sqliteConnection.cursor()

if __name__ == '__main__':
    add_bg_from_local('background.jpg')
    cursor = getConnection()
    # retreiving company names from database
    options = [x[0] for x in cursor.execute("SELECT DISTINCT e_company from emp") if x[0] != '']
    options = [' ']+options
    original_title = '<p style="font-family:Georgia; color:rgb(0, 0, 118); font-size: 50px;">Feedback First Review</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    comp = (st.selectbox('Select Company Name : ',(options))).lower()
    dicti = defaultdict(list)
    #dictionary for storing feedbacks based on sentiment analysis
    dicti["Positive"] = []
    dicti["Negative"] = []
    dicti["Neutral"] = []
    mx, neg, neu, pos = 0, 0, 0, 0

    if comp != "" :
        #Getting all the feedbacks of selected company
        cursor.execute('SELECT fb FROM emp where e_company = (?)', (comp,))
        ans = cursor.fetchall()
        cnt = 0
        for feedback in ans:
            #Checking if the feedback contains hate speech and display only if it does not contain hate speech
            h_output = client.detection(body={"document": {"text": feedback[0]}}, params={'detector': 'hate-speech', 'language': 'en'})
            l = (len(h_output.categories) == 0)
            if(feedback[0] and l):
                flag = 0
                text = feedback[0]
                #Using Emotional traits from NLP API to find emotion and perform sentimental analysis for the emotion
                output = client.classification(body={"document": {"text": text}}, params={'taxonomy':'emotional-traits','language':'en'})
                for category in output.categories:
                    flag = 1
                    cnt += 1
                    op = client.specific_resource_analysis(body={"document": {"text": category.label}},params={'language': 'en', 'resource': 'sentiment'})
                    #Classifying feedback based on sentiment score of the emotion
                    senti = op.sentiment.overall
                    if(senti < 0):
                        dicti["Negative"].append(feedback[0])
                        neg += 1
                    elif(senti == 0):
                        dicti["Neutral"].append(feedback[0])
                        neu += 1
                    else:
                        dicti["Positive"].append(feedback[0])
                        pos += 1
                if(flag == 0):
                    dicti["Neutral"].append(feedback[0])
        mx = max(neg, neu, pos)
        for x in dicti:
            l = len(dicti[x])
            for i in range(l, mx):
                dicti[x].append("-")
        st.text("Rating : ")
        rating = cursor.execute("SELECT AVG(rate) from emp where e_company = (?)", (comp,))
        for x in rating:
            st.text(x[0])
        df = pd.DataFrame(dicti)
        st.table(dicti)

        #For downloading reviews as excel document
        st.download_button('Download Reviews',data=pd.DataFrame.to_csv(df,index=False), mime="text/csv")
        oper = (st.selectbox('Show only : ',("Positive", "Negative", "Neutral")))

        #filtering reviews and displaying as table
        if dicti[oper]:
            if dicti[oper][0] != "-":
                st.table(dicti[oper])
            else:
                if oper == "Positive":
                    st.text("No Positive Reviews Yet")
                elif oper == "Negative":
                    st.text("No Negative Reviews Yet")
                else:
                    st.text("No Neutral Reviews Yet")
