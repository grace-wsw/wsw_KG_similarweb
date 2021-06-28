import streamlit as st
from PIL import Image



def app():

    # display image

    # show instructions
    st.title("Instructions \n")

    instructions = """
    1. put your URL links list as well as the date information in a csv/excel spreadsheet
    2. Change the column name to be the same as the template shown in "process" tab
    4. Upload the file and run the output
    5. Preview output and download data (The data will come in .csv )
    6. Upload another file to start the next job.
    
    ## Errors
    If you encounter any errors or have any questions, please reach out to Grace C. (gcai@webershandwick.com) or Aniz R. (aruda@webershandwick.com).
    """

    st.markdown(instructions)
    st.title("\n\n")
    image1 = Image.open("images/WS_logo.png")
    image2 = Image.open("images/GI_logo.png")
    image = Image.open("images/GI logo.png")
    st.image(image)
