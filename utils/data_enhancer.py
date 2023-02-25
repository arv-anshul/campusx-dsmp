""" Function to enhance the playlist data. """

import os
from json import dump, load

from pandas import DataFrame


def enhanced_playlist(file_path: str, store_data: bool = False, export_path: str | None = None):
    """ It get the data in json format which comes from the Youtube v3 API.\n
    Returns the enhanced data or store the data in given export path. """
    with open(file_path) as pl:
        pl_videos = load(pl)['items']

    # Get data as DataFrame
    playlist = DataFrame.from_dict(pl_videos)

    # Categorize the videos as `isPaid, isSession, isSolutions`
    playlist['isPaid'] = playlist['title'].apply(
        lambda x: 1 if 'Paid' in x else 0)

    playlist['isSolutions'] = playlist['title'].apply(
        lambda x: 1 if 'Solutions' in x or 'Task' in x else 0)

    playlist['isSession'] = playlist['title'].apply(
        lambda x: 1 if ('Session' in x or 'Paid' in x) and 'Solution' not in x else 0)

    # Get the 'Task Number' and 'Session Number'.
    playlist['sessionNo'] = (playlist['title']
                             .str.extract(r'Session (\d+)').astype(float))

    playlist['taskNo'] = (playlist['title']
                          .str.extract(r'Task (\d+)').astype(float))

    # Filtering `title` column.
    playlist['sessionName'] = (playlist['title']
                               .str.split('|', regex=False).str.get(0)
                               .str.split('-').str.get(-1)
                               .str.replace('Session on', '')
                               .str.strip())

    # Get data from `description` column.
    playlist['linkInVideo'] = (playlist['description']
                               .str.extractall(r'(https?:\/\/[^ ]*)')
                               .unstack()
                               .applymap(lambda x: x.split('\n')[0] if isinstance(x, str) else x)
                               .apply(lambda x: [i for i in x if isinstance(i, str)], axis=1)
                               )

    playlist['videoTimestamp'] = (playlist['description']
                                  .str.extractall(r'(\b(?:\d+:)?\d+:\d+\b .*)')
                                  .unstack()
                                  .applymap(lambda x: x.split('\n')[0] if isinstance(x, str) else x)
                                  .apply(lambda x: [i for i in x if isinstance(i, str)], axis=1)
                                  )

    # Datetime cols
    playlist = playlist.astype({
        'videoPublishedAt': 'datetime64',
        'addedToPlaylistAt': 'datetime64'
    })

    # --- Export the **enhanced** dataset. --- #
    if store_data and export_path:
        # Get the right form to export the dataset in json file
        # Also fill nan values with `<NaN>` for convience.
        new_playlist = {'items': list(playlist
                                      .fillna('<NaN>')
                                      .to_dict('index').values())}

        with open(export_path, 'w') as new_pl:
            return dump(new_playlist, new_pl, indent=2, sort_keys=True)

    return playlist


def enhanced_video_details(file_path: str, store_data: bool = False, export_path: str | None = None):
    """ It gets the data in json format which comes from the Youtube v3 API. 
    Returns the enhanced data or store the data in given export path. """
    with open(file_path) as f:
        vid_details = load(f)['items']

    # Read the data as DataFrame
    df = DataFrame.from_dict(vid_details)

    # Drop irrelevent cols
    df.drop(columns=['title', 'description', 'channelId', 'channelTitle', 'tags'],
            inplace=True)

    # Get length of video in minutes from duration column
    hour = df['duration'].str.extract(r'(\d)H').fillna(0).astype(int)
    minute = df['duration'].str.extract(r'(\d{2})M').fillna(0).astype(int)

    df['duration'] = hour.mul(60).add(minute)

    # Datetime cols
    df['publishedAt'] = df['publishedAt'].astype('datetime64')

    # --- Export the **enhanced** dataset. --- #
    if store_data and export_path:
        # Get the right form to export the dataset in json file
        # Also fill nan values with `<NaN>` for convience.
        new_vid_details = {'items': list(df
                                         .fillna('<NaN>')
                                         .to_dict('index').values())}

        with open(export_path, 'w') as new_pl:
            return dump(new_vid_details, new_pl, indent=2, sort_keys=True)

    return df


def merged_data(playlist_path, video_details_path):
    playlist = DataFrame(enhanced_playlist(playlist_path))
    video = DataFrame(enhanced_video_details(video_details_path))

    return (playlist
            .drop(columns=['description', 'title'])
            .merge(video.drop(columns=['publishedAt']),
                   how='inner', on='videoId'))
