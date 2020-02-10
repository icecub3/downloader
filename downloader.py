import os
import requests
from bs4 import BeautifulSoup
import datetime
import time

# specify the URL of the archive here
archive_url = "http://www.dinimizislam.com/detay.asp?Aid=13613"


def get_mp3_links():
    # create response object
    r = requests.get(archive_url)

    # create beautiful-soup object
    soup = BeautifulSoup(r.content, 'html5lib')

    # find all links on web-page
    links = soup.findAll('a')

    mp3_links = []
    for link in links:
        if 'href' in link.attrs.keys():
            if '.mp3' in link.attrs['href']:
                # print(link.attrs['href'])
                mp3_links += [link.attrs['href']]

    print(str(len(mp3_links)) + " links found.")
    return mp3_links


def download_mp3_series(mp3_links):
    print("Download started.")
    all_files_timer_start = time.perf_counter()
    for link in mp3_links:
        '''iterate through all links in video_links and download them one by one'''
        # obtain filename by splitting url and getting last string

        file_name = link.split('/')[-1]
        downloaded_file_name = os.getcwd() + "/downloaded/" + file_name
        now = datetime.datetime.now()
        print("Started to download file '" + file_name + "' at " + str(now) + ".")
        single_file_timer_start = time.perf_counter()
        # create response object
        r = requests.get(link, stream=True)

        # download started
        if not os.path.exists(downloaded_file_name):
            with open(downloaded_file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        single_file_timer_finish = time.perf_counter()
        single_file_total_time = single_file_timer_finish - single_file_timer_start
        print("Finished to download file '" + file_name + "' in " + str(single_file_total_time) + " seconds.")
    all_files_timer_finish = time.perf_counter()
    all_files_total_time = all_files_timer_finish - all_files_timer_start
    print("All files downloaded in " + str(all_files_total_time) + " seconds.")
    return


if __name__ == "__main__":
    # getting all mp3 links
    mp3_links = get_mp3_links()

    # download all mp3s
    download_mp3_series(mp3_links)
