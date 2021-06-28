#import re
import pandas as pd
from datetime import date 
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
