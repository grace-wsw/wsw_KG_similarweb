
import streamlit as st
import instructions
import process


PAGES = {"Instructions": instructions,"Process": process}
#"RFI Word Automation": AutomateWord,
st.set_page_config(
  page_title="SimilarWeb Integration",
  page_icon="🐣",
  initial_sidebar_state="expanded")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
