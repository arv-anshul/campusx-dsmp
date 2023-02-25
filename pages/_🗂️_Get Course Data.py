""" Fetches data from Youtube Data v3 API. """

# --- Imports --- #
from json import load

import streamlit as st
from googleapiclient.http import HttpError

from youtube_api.playlist import get_playlist_videos
from youtube_api.video import get_video_details

# --- Page config --- #
st.set_page_config('Data from API', '🗂️', 'wide')

# Info for data gathering from API using user's API_KEY
st.subheader(
    "This page requests data from **Youtube Data v3 API** using `API_KEY` (provide by you/user).")
st.text("Data stores in JSON format at repo path in your system in `data_from_st` folder.")

with st.form('api_form', True):
    API_KEY = st.text_input('Provide your **API_KEY** to fetch data from API',
                            type='password',
                            placeholder='API KEY HERE')
    playlist_id = st.text_input('**Playlist ID** of CampusX DSMP',
                                'PLKnIA16_RmvbAlyx4_rdtR66B7EHX5k3z')
    form_btn = st.form_submit_button()

if len(API_KEY) > 30 and form_btn:
    try:
        get_playlist_videos(API_KEY, playlist_id, True,
                            './data_from_st/playlist_st.json')
    except HttpError:
        st.error("Your API_KEY is not valid. Please provide valid KEY.", icon="🚨")
        exit()
    except KeyError as e:
        st.error(f"KeyError: {e}", icon="🔥")

    with open('./data_from_st/playlist_st.json') as pl:
        playlist = load(pl)['items']

        # list of video id
        id_list = [i['videoId'] for i in playlist]

    get_video_details(API_KEY, id_list, True,
                      './data_from_st/video_details_st.json')

    st.success('Your requested data has been saved. Now see the analysis.',
               icon="✅")
