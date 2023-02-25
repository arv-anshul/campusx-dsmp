""" Uses google_api module to get data and store them into files. """

import json
import os

from youtube_api.playlist import get_playlist_videos
from youtube_api.video import get_video_details

API_KEY = os.environ['YOUTUBE_APIs']
PL_ID = 'PLKnIA16_RmvbAlyx4_rdtR66B7EHX5k3z'

playlist_path = './data/playlist_new.json'
video_details_path = './data/video_details_new.json'

get_playlist_videos(API_KEY, PL_ID, True, playlist_path)
print('Playlist Complete!')

with open(playlist_path, 'r') as pl:
    data = json.load(pl)['items']

    id_list = [i['videoId'] for i in data]

get_video_details(API_KEY, id_list, True, video_details_path)
print('Done!')
