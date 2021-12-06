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
        genre2 = st.radio("what's your target traffic?",("Desktop","Mobile","Desktop+Mobile"))
        st.header("Upload File (only one at a time): \n")
        st.text(
            """Upload one URL list you'd like to process (.csv, .xlsx)
            (Default audience is US only.)"""
        )


        if genre1 !='impression by month (monthly unique visitors)':
            st.write("Sorry, current selection is unavailable at this time")

        if genre1 == 'impression by month (monthly unique visitors)':
            uploadedfile = st.file_uploader(
                "File Uploader", accept_multiple_files=False
            )

            if uploadedfile:
                df = helpers.read_data(uploadedfile)
                df.columns = df.columns.map(lambda col_name: col_name.replace(' ', '').capitalize())
                #if isinstance(col_name, str) else col_name
                df.drop_duplicates(subset=['Link'],inplace=True)
                df['Domain']=df['Link'].apply(lambda x:helpers.domain_plus(x))
                df['Date']= pd.to_datetime(df['Date']) 
                df['key'] = df[['Domain', 'Date']].values.tolist()
                save_date = datetime.strftime(datetime.now(),'%Y-%m-%d')
                if genre2 == "Desktop":
                    output =  helpers.get_desktop_traffic(df)
                    output.drop(columns=['key','tuplekey'],inplace=True)
                if genre2 == "Mobile":
                    output = helpers.get_mobile_traffic(df)
                    output.drop(columns=['key','tuplekey'],inplace=True)
                if genre2 == "Desktop+Mobile":
                    desktop_traffic = helpers.get_desktop_traffic(df)
                    output = helpers.get_mobile_traffic(desktop_traffic)
                    output["SWMonthlyUniqueVisitors(US,Desktop+Mobile)"] = output["SWMonthlyUniqueVisitors(US,Desktop)"] + output["SWMonthlyUniqueVisitors(US,Mobile)"]  
                    output.drop(columns=['key','tuplekey'],inplace=True)

                st.write(output)
                    # write to file for download
                csv_download_link = helpers.download_link(
                    output,
                    "{}_tracker_filled_{}.csv".format(genre2,save_date),
                    "Click here to download filled tracker in .csv by our automation!",
                )
                st.text(
                """your output in .csv can be downloaded here👇""")
                st.markdown(csv_download_link, unsafe_allow_html=True)
