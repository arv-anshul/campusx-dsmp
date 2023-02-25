""" APIs for youtube videos to get descriptions, runtime, views, etc. """

import logging
import os
from json import dump

from googleapiclient.discovery import build


def get_video_details(API_KEY,
                      video_id: list[str],
                      store_data: bool = False,
                      file_path: str | None = None):
    """Get the `'description', 'title' and 'video_id'` of the youtube video by providing `API_KEY`.

This function uses `logging` module to make logs when the video is 'deleted' or 'unavaiable' in API.
Logs are available in `./logs` folder.

    Args:
        API_KEY (str): Provide your `Youtube v3` API_KEY.
        video_id (str): Any video's id. Get it from its URL.
        store_data (bool, optional): If you want to store the video data in json file set the value as 'True'. Defaults to False.
        filename (str | None, optional): If store_data is 'True' the provide filename to store the data in json format. Defaults to None.

    Returns:
        dict[str, list]: Get the video title and video_id in list of dictonary format.

        None: Returns when you store the data in json file.

    ---
    Get a video data in dictionary object:
    ```python
        >>> from google_api.youtube.video import get_video_details
        >>> 
        >>> PL_ID = 'PLKnIA16_RmvbAlyx4_rdtR66B7EHX5k3z'
        >>> 
        >>> # Get a dictionary with video's description, title and video_id
        >>> get_video_details(API_KEY, PL_ID)
    ```

    Store the data into a json file:
    ```python
        >>> # Store the API data in json file.
        >>> get_video_details(API_KEY, PL_ID,
                                stror_data=True,
                                filename='video_data.json')   # Returns None
    ```

    ---
    Also, `id` parameter can be provided with `,` separated.
    """
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Dictanory to store video details
    video_details_dict = {'video_details': []}

    # Logging the error in file
    if not os.path.isdir('./logs'):
        os.mkdir('./logs')

    logging.basicConfig(filename='./logs/get_video_details.log',
                        level=logging.ERROR,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    for _id in video_id:
        request = youtube.videos().list(part='snippet,contentDetails,statistics', id=_id)
        response = request.execute()

        # Check whether video is not deleted or available
        try:
            video = response['items'][0]
        except IndexError:
            # Log the error
            logging.error(f"video_id='{_id}' is unavialabel or deleted.")

            # Append the data as deleted video.
            video_details_dict['video_details'].append({
                'videoId': _id,
                'channelId': None,
                'channelTitle': None,
                'title': 'Deleted Video',
                'description': None,
                'tags': None,
                'categoryId': None,
                'duration': None,
                'viewCount': None,
                'likeCount': None,
                'commentCount': None
            })
            continue

        publishedAt = video['snippet']['publishedAt']
        title = video['snippet']['title']
        description = video['snippet']['description']
        channelId = video['snippet']['channelId']
        channelTitle = video['snippet']['channelTitle']
        try:
            tags = ', '.join(video['snippet']['tags'])
        except KeyError:
            tags = None
        categoryId = video['snippet']['categoryId']

        duration = video['contentDetails']['duration']

        # For members only video viewCount is hidden for publics
        try:
            viewCount = int(video['statistics']['viewCount'])
        except KeyError:
            viewCount = None

        likeCount = video['statistics']['likeCount']
        commentCount = video['statistics']['commentCount']

        # Append the details
        video_details_dict['video_details'].append({
            'videoId': _id,
            'publishedAt': publishedAt,
            'channelId': channelId,
            'channelTitle': channelTitle,
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': int(categoryId),
            'duration': duration,
            'viewCount': viewCount,
            'likeCount': int(likeCount),
            'commentCount': int(commentCount)
        })

    if store_data and file_path:
        # Check wheter the folder exists if not then create it.
        if not os.path.exists('./data_from_st'):
            os.mkdir('./data_from_st')

        # Store requested videos data in json file
        with open(file_path, 'w') as f:
            return dump(video_details_dict, f, indent=2, sort_keys=True)

    return video_details_dict
