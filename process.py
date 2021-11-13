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
    #create template

    #template = pd.DataFrame(columns=["Link","Date"])
        d = {"Link": ["https://www.XYZ.com/this_is_just_an_example_Link", "www.XYZ.com/this_format_is_also_acceptable"], "Date": ["2021/03/21", "03/21"]}
        template = pd.DataFrame(data=d)
        # display image
        #image = Image.open("images/ab_ws_logo.png")
        #st.image(image, use_column_width=True)

        # general info
        st.title("SimilarWeb automation \n")
        st.header("Please use below header for your list: \n")
        st.dataframe(template)
        genre1 = st.radio("what's your target metric?",("impression by month (monthly unique visitors)","website ranking"))
        genre2 = st.radio("what's your target traffic?",("Desktop","Mobile"))
        st.header("Upload File (only one at a time): \n")
        st.text(
            """Upload one URL list you'd like to process (.csv, .xlsx)
            (Default audience is US only.)"""
        )


        if genre1 !='impression by month (monthly unique visitors)' or genre2 != 'Desktop' :
            st.write("Sorry, current selection is unavailable at this time")

        if genre1 == 'impression by month (monthly unique visitors)' and genre2 == 'Desktop':
            uploadedfile = st.file_uploader(
                "File Uploader", accept_multiple_files=False
            )

            if uploadedfile:
                df = helpers.read_data(uploadedfile)
                df.columns = df.columns.map(lambda col_name: col_name.replace(' ', '') if isinstance(col_name, str) else col_name)
                df['Domain']=df['Link'].apply(lambda x:helpers.domain_plus(x))
                df['Date']= pd.to_datetime(df['Date']) 

                df['key'] = df[['Domain', 'Date']].values.tolist()
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
                df.drop(columns=['key','tuplekey'],inplace=True)



                st.write(df)

                    # write to file for download
                csv_download_link = helpers.download_link(
                    df,
                    "tracker_filled_{}.csv".format(save_date),
                    "Click here to download filled tracker in .csv by our automation!",
                )
                st.text(
                """your output in .csv can be downloaded here👇""")
                st.markdown(csv_download_link, unsafe_allow_html=True)
        
