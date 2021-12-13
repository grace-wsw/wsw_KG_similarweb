import pandas as pd
import helpers
#import errors
#import yaml
import tldextract
import streamlit as st
import tldextract
from dateutil.parser import parse
from datetime import datetime
import requests
from dateutil.relativedelta import relativedelta, MO
#from PIL import Image


def app():
    password = st.text_input('Enter the password to continue')
    if password == st.secrets["PASSWORD"]:
    #if password == "Weber2021!":
    #create template
        st.header("the website now has been updated to: https://share.streamlit.io/wsw-global-intelligence-products/kg_similarweb_app/main/app.py")

        
