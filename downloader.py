from bs4 import BeautifulSoup
import datetime
import os
import requests
import time

# Specify the URL of the page that you want to search
archive_url = "http://www.dinimizislam.com/detay.asp?Aid=13613"


# Crawls into given archive_url and collects file URLs with '.mp3'.
def get_mp3_links():
    response = requests.get(archive_url)
    soup = BeautifulSoup(response.content, 'html5lib')  # Using BeautifulSoup library to pull the data out
    links = soup.findAll('a')                           # Pull all <a> tags from the web page
    mp3_links = []                                      # Filter the data and collect the .mp3 links
    for link in links:
        if 'href' in link.attrs.keys():
            if '.mp3' in link.attrs['href']:
                # print("DEBUG::link.attrs['href']:" + str(link.attrs['href']))
                mp3_links += [link.attrs['href']]
    print(str(len(mp3_links)) + " links found.")
    return mp3_links


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
#TODO: Make a simple command line interface to get URL
if __name__ == "__main__":
    download_mp3_series(get_mp3_links())
    input('Press a button to exit.')
