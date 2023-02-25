""" To fecth details of youtube playlists. """

import os
from json import dump

from googleapiclient.discovery import build


def get_playlist_videos(API_KEY: str,
                        playlist_id: str,
                        store_data: bool = False,
                        file_path: str | None = None):
    """Get the Youtube Playlsit's all video's `title` and `video_id` with `API_KEY` and `playlist_id`.

    Args:
        API_KEY (str): Provide your `Youtube v3` API_KEY.
        playlist_id (str): Any playlist's id. Get it from its URL.
        store_data (bool, optional): If you want to store the playlist data in json file set the value as 'True'. Defaults to False.
        filename (str | None, optional): If store_data is 'True' the provide filename to store the data in json format. Defaults to None.

    Returns:
        list[dict[str, str]]: Get the video title and video_id in list of dictonary format.

        None: Returns when you store the data in json file.

    ---
    Get a list of dicts:
    ```python
        >>> from google_api.youtube.playlist import get_playlist_videos
        >>> 
        >>> PL_ID = 'PLKnIA16_RmvbAlyx4_rdtR66B7EHX5k3z'
        >>> 
        >>> # Get a list of dictionary with playlist's videos title and video_id
        >>> get_playlist_videos(API_KEY, PL_ID)   # Returns list of dict.
    ```

    Store the data into a json file:
    ```python
        >>> # Store the API data in json file.
        >>> get_playlist_videos(API_KEY, PL_ID,
                                stror_data=True,
                                filename='playist_data.json')   # Returns None
    ```
    """

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        maxResults=50,
        playlistId=playlist_id
    )
    videos = []
    while request is not None:
        response = request.execute()
        # Append video details
        videos += response['items']
        request = youtube.playlistItems().list_next(request, response)

    # Create list to store title and video_id
    video_details = {'items': []}

    for video in videos:
        videoId = video['contentDetails']['videoId']
        title = video['snippet']['title']

        # Check whether video is deleted or not
        try:
            videoPublishedAt = video['contentDetails']['videoPublishedAt']
        except KeyError:
            video_details['items'].append({
                'videoId': videoId,
                'videoPublishedAt': None,
                'title': title,
                'description': None,
                'addedToPlaylistAt': None,
            })
            continue

        description = video['snippet']['description']
        addedToPlaylistAt = video['snippet']['publishedAt']

        video_details['items'].append({
            'videoId': videoId,
            'videoPublishedAt': videoPublishedAt,
            'title': title,
            'description': description,
            'addedToPlaylistAt': addedToPlaylistAt,
        })

    if store_data and file_path:
        # Check wheter the folder exists if not then create it.
        if not os.path.exists('./data_from_st'):
            os.mkdir('./data_from_st')

        # Store playlist video details in json file
        with open(file_path, 'w') as f:
            return dump(video_details, f, indent=2, sort_keys=True)

    return video_details
