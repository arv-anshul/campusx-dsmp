""" Function to downlaod the tasks `colab notebooks` of CampusX DSMP. """

# Imports
from pathlib import Path
from typing import Literal

from data_enhancer import enhanced_playlist
from pandas import NA, DataFrame
from requests import get


def download_drive_files(url: str, file_path: str | Path):
    # Get the ID of the file
    url = url.rsplit('/', 1)[-1].split('?')[0]

    # Prefix for download url
    dl_prefix = 'https://docs.google.com/uc?export=download&id='

    print(dl_prefix + url)

    # Request the file with its download url
    r = get(dl_prefix + url)

    # Write the file with chunks
    with open(file_path, 'wb') as pdf:
        for chunk in r.iter_content(5000):
            pdf.write(chunk)


def download_notebook(data_file_path: str,
                      save_to_folder: str | Path,
                      type: Literal['solution', 'task'] = 'task'):
    query = 'isSession==1' if type == 'task' else 'isSolutions==1'

    df = DataFrame(enhanced_playlist(data_file_path)).query(query)

    df['linkInVideo'] = (df['linkInVideo'][df['linkInVideo'].isnull() == 0]
                         .apply(lambda x: [i for i in x if 'colab' in i]))

    # Convert the string path to Path object
    if isinstance(save_to_folder, str):
        save_to_folder = Path(save_to_folder)

    # Check given folder exists if not create one
    if not save_to_folder.exists():
        save_to_folder.mkdir()

    for filename, notebook_urls in df[['sessionName', 'linkInVideo']].values:
        # Check if there is no url
        if len(notebook_urls) == 0:
            continue

        # Check if more than 1 url
        if len(notebook_urls) > 1:
            for i, nblink in enumerate(notebook_urls):
                if not 'colab' in nblink:
                    continue
                download_drive_files(nblink,
                                     save_to_folder / f'{filename}-{i}.ipynb')
        else:
            if not 'colab' in (url := notebook_urls[0]):
                continue
            download_drive_files(url,
                                 save_to_folder / f'{filename}.ipynb')
        break


def download_nb_for(data_file_path: str,
                    type: Literal['task', 'session'],
                    n: int,
                    save_to_folder: str | Path):
    query = 'sessionNo==@n' if type == 'task' else 'taskNo==@n'
    df = DataFrame(enhanced_playlist(data_file_path)).query(query)

    filename = str(df['sessionName'].values[0])
    notebook_urls = [i for i in df['linkInVideo'].values if 'colab' in i]

    if not isinstance(save_to_folder, Path):
        save_to_folder = Path(save_to_folder)

    for url in notebook_urls:
        # If video has more than one notebooks.
        i = None
        if len(notebook_urls) > 1:
            i = 1

        if i:
            if 'colab' in url:
                download_drive_files(url,
                                     save_to_folder / (filename+str(i)+'.ipynb'))

        if 'colab' in url:
            download_drive_files(url, save_to_folder / (filename+'.ipynb'))


if __name__ == '__main__':
    # download_notebook('data/playlist_new.json', 'notebooks')
    # download_nb_for('data/playlist_new.json', 'task', 4, 'notebooks')

    pass
