#import re
import pandas as pd
from datetime import date
from datetime import datetime
import requests
from dateutil.relativedelta import relativedelta, MO 
import base64
import os
from io import BytesIO
#import torch
from collections import OrderedDict
import tldextract


'''
def getScore(torchTensor):
	tem = re.findall(r"[-+]?\d*\.?\d+|\d+", str(torchTensor))
	return round(float(tem[0]), 4)
'''

def domain_plus(URL):
    
    if isinstance(URL,str):
        extract = tldextract.extract(URL.replace("://eu.","://www."))

        if (extract.subdomain != 'www') and (extract.subdomain != ""):
            return ".".join([extract.subdomain, extract.domain, extract.suffix])
        
        else:
            return ".".join([extract.domain, extract.suffix])


def read_data(data_path):
    """
    Returns data from file (csv or excel) to dataframe.
    Parameters:
        data_path (str): path to file
    Returns:
        df (pd.DataFrame): pandas dataframe of raw data
    """

    # read raw data
    try:
        df = pd.read_csv(data_path)
    except:
        try:
            df = pd.read_excel(data_path, engine='openpyxl')
        except:
            df = pd.read_excel(data_path, engine='openpyxl')

    df.columns = [c.lstrip().rstrip() for c in df.columns]
    return df



def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.
    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.
    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode("utf-8")).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def get_desktop_traffic(df):
    lookup_dict = [x for x in df['key']]
    lookup_dict = [tuple(item) for item in lookup_dict]
    lookup_dict = list(set(lookup_dict))
    lookup_dict = [list(item) for item in lookup_dict]

    this_month = datetime.date(datetime.now()).strftime("%Y-%m")
    save_date = datetime.strftime(datetime.now(),'%Y-%m-%d')
    impression_dic = {}
    for i in lookup_dict:
        try:
            if str(i[1].strftime("%Y-%m"))==this_month:
                start_date=str((i[1]-relativedelta(months=1)).strftime("%Y-%m"))
                payload = {'api_key': st.secrets["SIMILARWEB_API_KEY"], 
                       'start_date': start_date, 
                       'end_date': start_date, 
                       'country': 'US', 
                       'granularity': 'monthly', 
                       'main_domain_only': 'false', 
                       'format': 'json'}
                url= 'https://api.similarweb.com/v1/website/'+i[0]+'/unique-visitors/desktop_unique_visitors'
                r=requests.get(url,params=payload)
                impression= r.json()['unique_visitors'][0]['unique_visitors']
                impression_dic.update({tuple(i):impression})
            else:
                start_date=str(i[1].strftime("%Y-%m"))
                end_date=str(i[1].strftime("%Y-%m"))
                payload = {'api_key': st.secrets["SIMILARWEB_API_KEY"],
                       'start_date': start_date, 
                       'end_date': end_date, 
                       'country': 'US', 
                       'granularity': 'monthly', 
                       'main_domain_only': 'false', 
                       'format': 'json'}
                url= 'https://api.similarweb.com/v1/website/'+i[0]+'/unique-visitors/desktop_unique_visitors'
                r=requests.get(url,params=payload)
                impression_dic.update({tuple(i):r.json()['unique_visitors'][0]['unique_visitors']})
        except:
            impression='error code 401, data not found'
            impression_dic.update({tuple(i):impression})
    df['tuplekey'] = df['key'].apply(lambda x:tuple(x))
    df['data_source_month']=df['Date'].apply(lambda x:'Previous Month'if x.strftime("%Y-%m")==this_month else x.strftime("%Y-%m") )        
    df['SWMonthlyUniqueVisitors(US,Desktop)']=df['tuplekey'].apply(lambda x:impression_dic[x])
    #df.drop(columns=['key','tuplekey'],inplace=True)
    return df

def get_mobile_traffic(df):
    lookup_dict = [x for x in df['key']]
    lookup_dict = [tuple(item) for item in lookup_dict]
    lookup_dict = list(set(lookup_dict))
    lookup_dict = [list(item) for item in lookup_dict]

    this_month = datetime.date(datetime.now()).strftime("%Y-%m")
    save_date = datetime.strftime(datetime.now(),'%Y-%m-%d')
    impression_dic = {}
    for i in lookup_dict:
        try:
            if str(i[1].strftime("%Y-%m"))==this_month:
                start_date=str((i[1]-relativedelta(months=1)).strftime("%Y-%m"))
                payload = {'api_key': st.secrets["SIMILARWEB_API_KEY"], 
                       'start_date': start_date, 
                       'end_date': start_date, 
                       'country': 'US', 
                       'granularity': 'monthly', 
                       'main_domain_only': 'false', 
                       'format': 'json'}
                url= 'https://api.similarweb.com/v1/website/'+i[0]+'/unique-visitors/mobileweb_unique_visitors'
                r=requests.get(url,params=payload)
                impression= r.json()['unique_visitors'][0]['unique_visitors']
                impression_dic.update({tuple(i):impression})
            else:
                start_date=str(i[1].strftime("%Y-%m"))
                end_date=str(i[1].strftime("%Y-%m"))
                payload = {'api_key': st.secrets["SIMILARWEB_API_KEY"], 
                       'start_date': start_date, 
                       'end_date': end_date, 
                       'country': 'US', 
                       'granularity': 'monthly', 
                       'main_domain_only': 'false', 
                       'format': 'json'}
                url= 'https://api.similarweb.com/v1/website/'+i[0]+'/unique-visitors/mobileweb_unique_visitors'
                r=requests.get(url,params=payload)
                impression_dic.update({tuple(i):r.json()['unique_visitors'][0]['unique_visitors']})
        except:
            impression='error code 401, data not found'
            impression_dic.update({tuple(i):impression})
    df['tuplekey'] = df['key'].apply(lambda x:tuple(x))
    df['data_source_month']=df['Date'].apply(lambda x:'Previous Month'if x.strftime("%Y-%m")==this_month else x.strftime("%Y-%m") )        
    df['SWMonthlyUniqueVisitors(US,Mobile)']=df['tuplekey'].apply(lambda x:impression_dic[x])
    #df.drop(columns=['key','tuplekey'],inplace=True)
    return df