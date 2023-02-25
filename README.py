""" README page for CampusX DSMP course dashbord making and analysis project. """

import streamlit as st

# Page config
st.set_page_config('README.md', '🗒️', 'wide')

# Read the markdown file to display.
with open('README.md', 'r') as md:
    st.markdown(md.read())
