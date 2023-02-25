# --- Imports --- #
import os

import streamlit as st

from utils.data_enhancer import merged_data

# --- Page config --- #
st.set_page_config('Overview of the data', '💬', 'wide')

# Choose dataset
# Wheter to use user's data or pre-provided data
if os.path.exists('./data_from_st'):
    playlist_path = './data_from_st/playlist_st.json'
    video_ditails_path = './data_from_st/video_details_st.json'
else:
    playlist_path = './data/playlist_enhanced_new.json'
    video_ditails_path = './data/video_details_new.json'

df = merged_data(playlist_path, video_ditails_path)
