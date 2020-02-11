from bs4 import BeautifulSoup
import datetime
import os
import requests
import time


# Crawls into given archive_url and collects file URLs with given file type
# TODO: It needs to be reworked
def get_file_links(archive_url, file_type):
    response = requests.get(archive_url)
    soup = BeautifulSoup(response.content, 'html5lib')  # Using BeautifulSoup library to pull the data out
    links = soup.findAll('a')                           # Pull all <a> tags from the web page
    links_to_download = []                              # Filter the data and collect the given extension links
    for link in links:
        if 'href' in link.attrs.keys():
            if file_type in link.attrs['href']:
                # print("DEBUG::link.attrs['href']:" + str(link.attrs['href']))
                links_to_download += [link.attrs['href']]
    print(str(len(links_to_download)) + " links found.")
    return links_to_download


# Downloads given files to the '/downloaded' directory.
def download_mp3_series(mp3_links):
    print("Download started.")
    all_files_timer_start = time.perf_counter()
    for link in mp3_links:
        file_name = link.split('/')[-1]
        downloaded_file_name = os.getcwd() + "/downloaded/" + file_name
        now = datetime.datetime.now()
        print("Started to download file '" + file_name + "' at " + str(now) + ".")
        single_file_timer_start = time.perf_counter()
        response = requests.get(link, stream=True)
        # TODO: Find a better way to copy files.
        if not os.path.exists(downloaded_file_name):
            with open(downloaded_file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        single_file_timer_finish = time.perf_counter()
        single_file_total_time = single_file_timer_finish - single_file_timer_start
        print("Finished to download file '" + file_name + "' in " + str(single_file_total_time) + " seconds.")
    all_files_timer_finish = time.perf_counter()
    all_files_total_time = all_files_timer_finish - all_files_timer_start
    print("All files downloaded in " + str(all_files_total_time) + " seconds.")
    return


# Driver method
if __name__ == "__main__":
    archive_url = input('Enter the page URL which you want to crawl into its HTML:')
    file_type = input('Enter the file extension for the files which you want to download:')
    print('downloader will download the files with "' + file_type + '" in "' + archive_url + '".')
    # download_mp3_series(get_file_links('http://www.dinimizislam.com/detay.asp?Aid=13613', '.mp3'))
    download_mp3_series(get_file_links(archive_url, file_type))
