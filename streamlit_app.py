import streamlit as st
import random
import json

import torch
import nltk

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import string
import urllib
from bokeh.models.widgets import Div
from urllib.request import Request, urlopen
import time
import re
import urllib
from PIL import Image
nltk.download('punkt')
st.set_page_config(layout="wide")
headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
st.markdown("""<style>body {background-color: #9AE6F6;}</style>""", unsafe_allow_html=True)

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Covibot"
# st.title('   🔥🔥🔥🔥 COVIDBOT BY AMITY GROUP-7 🔥🔥🔥🔥')
st.markdown("<h1 style='text-align: center; color: black;'>🔥🔥🔥 COVID-BOT BY AMITY GROUP-7 🔥🔥🔥</h1>", unsafe_allow_html=True)
z=0
sentence =  st.text_area('You:')
if sentence:
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    z = 0
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag=='Covid bed status':

                try:
                    col1, col2 = st.beta_columns([1, 4])
                    if(z==0):
                        image = Image.open('Covibot-photo.png')
                        col1.write("")
                        col1.write("Covibot:")
                        col1.image(image, width=255)
                    z=z+1
                    col2.write("")
                    col2.write("")
                    col2.text_area("  ", value="Select the cities or enter the cities in other", height=200,
                                   max_chars=None,
                                   key=None)
                    city = st.selectbox("Select cities", ['Delhi', 'Navi Mumbai', 'Surat', 'Ahemdabad', 'Vadodara','Other'])
                    if city== 'Vadodara':
                        js = "window.open('{}')".format('https://vmc.gov.in/covid19vadodaraapp/')  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                    if city=='Other':
                        i=st.text_input("Enter city Name")
                    if city=='Ahemdabad':
                        js = "window.open('{}')".format('https://ahmedabadcity.gov.in/portal/web?requestType=ApplicationRH&actionVal=loadCoronaRelatedDtls&queryType=Select&screenId=114')  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                    if city== 'Surat':
                        text = '(Click here to download the list)'
                        url = 'https://ahna.org.in/'
                        plist = []
                        temp = requests.get(
                            'http://office.suratsmartcity.com/suratcovid19/home/covid19bedavailabilitydetails',
                            headers=headers)
                        temp = BeautifulSoup(temp.text, 'html.parser')
                        temp = temp.find_all('a', {'class': 'hospital-info'})
                        # temp_club = temp_club.find_all('a')
                        for p in temp:
                            if p.has_attr('href'):
                                # if (p.text):
                                try:
                                    # n = p.text
                                    # n='n'
                                    # p = (p['href'])

                                    plist.append(p.text)
                                    # elif (plyr.text == f2)
                                except:
                                    print("")
                        plist = [w.replace('  Contact', '') for w in plist]
                        vlist = []
                        temp = requests.get(
                            'http://office.suratsmartcity.com/suratcovid19/home/covid19bedavailabilitydetails',
                            headers=headers)
                        temp = BeautifulSoup(temp.text, 'html.parser')
                        temp = temp.find_all('span', {'class': 'count-text pr-2'})
                        # temp_club = temp_club.find_all('a')
                        for p in temp:

                            # if (p.text):
                            try:
                                # n = p.text
                                # n='n'
                                # p = (p['href'])

                                vlist.append(p.text)
                                # elif (plyr.text == f2)
                            except:
                                print("")
                        vlist = [w.replace('Total Vacant - ', '') for w in vlist]
                        surat_dict = {}
                        df_surat = pd.DataFrame(columns=['Hospital', 'Vacant Beds'])
                        for i in range(0, len(vlist)):
                            if (int(vlist[i]) > 0):
                                df_surat.loc[len(df_surat.index)] = [plist[i], int(vlist[i])]
                        df_surat.sort_values(by=['Vacant Beds'], ascending=False, inplace=True)
                        df_surat.reset_index(inplace=True, drop=True)
                        my_expander = st.beta_expander("Table")
                        my_expander.write(df_surat)
                    if city=='Delhi':

                        url = 'https://coronabeds.jantasamvad.org/covid-info.js'
                        req = Request(url, headers=headers)
                        html = urlopen(req)
                        temp = requests.get(url, headers=headers)
                        temp = BeautifulSoup(temp.text, 'html.parser')
                        urllib.request.urlretrieve(url, 'data.js')

                        js = open("data.js", "r")
                        # tcount= 0
                        # for k in js:
                        #     if(k=='    "All": {\n'):
                        #         break
                        #     tcount+=1

                        count1 = 0
                        vcount = 7
                        ncount = 2
                        lcount = 0
                        v_list = []
                        n_list = []
                        for j in js:
                            if (j == '    "All": {\n'):
                                break
                            if (lcount == ncount):
                                n_list.append(j)
                                ncount += 7
                            if (lcount == vcount):
                                v_list.append(j)
                                vcount += 7

                            lcount += 1
                        n_list = [w.replace('    "', '') for w in n_list]
                        n_list = [w.replace('": {\n', '') for w in n_list]
                        v_list = [w.replace('      "vacant": ', '') for w in v_list]
                        v_list = [w.replace('\n', '') for w in v_list]
                        delhi_df = pd.DataFrame(columns=['Hospital', 'Vacancy'])
                        for i in range(0, len(v_list)):
                            if (int(v_list[i]) > 0):
                                delhi_df.loc[len(delhi_df.index)] = [n_list[i], int(v_list[i])]
                        delhi_df.sort_values(by=['Vacancy'], ascending=False, inplace=True)
                        delhi_df.reset_index(inplace=True, drop=True)
                        my_expander = st.beta_expander("Table")
                        my_expander.write(delhi_df)
                    if city=='Navi Mumbai':
                        js = "window.open('{}')".format('https://www.nmmchealthfacilities.com/HospitalInfo/showhospitalist')  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                    if city=='Other':
                        i=st.text_input("Enter city Name")
                        if i:
                            js = "window.open('https://twitter.com/search?q={}+%28bed+OR+beds%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(i)  # New tab or window
                            html = '<img src onerror="{}">'.format(js)
                            div = Div(text=html)
                            st.bokeh_chart(div)

                except:
                    st.write("")

            elif tag == 'Covid Oxygen':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Select the cities or enter the cities in other", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q={}+%28oxygen%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")

            elif tag == 'Covid ICU':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Please Enter the city", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q={}+%28icu%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")
            elif tag == 'Covid Ventilator':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Please Enter the city", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q={}+%28ventilator+OR+ventilators%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")
            elif tag == 'Covid Tests':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Please Enter the city", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q={}+%28test+OR+tests+OR+testing%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(
                            k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")
            elif tag == 'Covid Fabiflu':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Please Enter the city", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q=verified+{}+%28fabiflu%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")
            elif tag == 'Covid Remdesivir':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Please Enter the city", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q=verified+{}+%28remdesivir%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")
            elif tag == 'Covid Favipiravir':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Please Enter the city", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q=verified%20{}%20(favipiravir)%20%20-%22needed%22%20-%22need%22%20-%22needs%22%20-%22required%22%20-%22require%22%20-%22requires%22%20-%22requirement%22%20-%22requirements%22&src=typed_query&f=live')".format(k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")
            elif tag == 'Covid Tocilizumab':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Please Enter the city", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q=verified+{}+%28tocilizumab%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")
            elif tag == 'Covid Plasma':
                col1, col2 = st.beta_columns([1, 4])
                if (z == 0):
                    image = Image.open('Covibot-photo.png')
                    col1.write("")
                    col1.write("Covibot:")
                    col1.image(image, width=255)
                z = z + 1
                col2.write("")
                col2.write("")
                try:
                    col2.text_area("  ", value="Please Enter the city", height=200,
                                   max_chars=None,
                                   key=None)
                    k = st.text_input("Enter your city Name")
                    if k:
                        js = "window.open('https://twitter.com/search?q=verified+{}+%28plasma%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live')".format(k)  # New tab or window
                        html = '<img src onerror="{}">'.format(js)
                        div = Div(text=html)
                        st.bokeh_chart(div)
                except:
                    st.write("")





            elif tag == intent["tag"]:
                col1, col2 = st.beta_columns([1,4])
                image = Image.open('Covibot-photo.png')
                col1.write("")
                col1.write("Covibot:")
                col1.image(image, width=255)
                col2.write("")
                col2.write("")
                col2.text_area("", value=random.choice(intent['responses']), height=200, max_chars=None, key=None)
    else:
        col1, col2 = st.beta_columns([1, 4])
        image = Image.open('Covibot-photo.png')
        col1.write("")
        col1.write("Covibot:")
        col1.image(image, width=255)
        col2.write("")
        col2.write("")
        col2.text_area("", value="Sorry i dont understand,please write again", height=200, max_chars=None, key=None) 
           

# st.markdown("<h2>Demo video on how this website works</h2>",unsafe_allow_html=True)
# # video_file = open('video.mp4', 'rb')
# video_bytes = video_file.read()
# st.video(video_bytes)
# st.write("We are here to only provide information,not verify them") 
# st.subheader(' -----------------Created By : (Prabhat, Shivam, Pankaj, Saurabh) ----------------- :sunglasses:')
# st.markdown("<h3>Created By Prabhat,Shivam,Pankaj,Saurabh</h3>",unsafe_allow_html=True)
# st.markdown("<h2 color: black;'>Features of Covid Bot</h2>", unsafe_allow_html=True)
# st.markdown("<h4 color: black;'>1. Ask FAQ's related to Covid-19</h4>", unsafe_allow_html=True)
# st.markdown("<h4 color: black;'>2. Get the current bed availibility in your city</h4>", unsafe_allow_html=True)
# st.markdown("<h4 color: black;'>3. Get a link of a twitter search wherein you can get tweets about information regarding availibility of beds,medicines and oxygen</h4>", unsafe_allow_html=True)
# st.markdown("<h4 color: black;'>4. Get the current COVID-19 status in your city</h4>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: red;'>Created By : (Prabhat, Shivam, Pankaj, Saurabh) 😎😎</h4>", unsafe_allow_html=True)
