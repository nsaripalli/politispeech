#! /usr/bin/python3
from time import sleep
import click
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def clean_transcript(raw_transcript: str):
    soup = BeautifulSoup(raw_transcript, 'html.parser')
    return "".join([i.get_text() for i in soup.find_all('a', class_='transcript-time-seek')]).lower()


def transcipt_scraper(video__url: str):
    api_endpoint = "{}{}".format(video__url,
                                 "&action=getTranscript&transcriptType=cc&service-url=/common/services/programSpeakers"
                                 ".php&appearance-filter=&personSkip=0&ccSkip=0&transcriptSpeaker=&transcriptQuery=#")

    raw_transcript = requests.get(api_endpoint, allow_redirects=True).content

    return clean_transcript(raw_transcript)


def get_links_from_c_span_url(c_span_search_url, load_more):
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(c_span_search_url)

    if load_more:
        while True:
            try:
                # Scroll down to bottom of page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loadmore')))
                driver.find_element_by_id("loadmore").click()
            except StaleElementReferenceException:
                print("Done loading more videos")
                break

    raw_thumbnails = driver.find_element_by_class_name("video-results").find_elements_by_class_name('thumb')
    links = [thumbnail.get_attribute('href') for thumbnail in raw_thumbnails]

    driver.quit()

    return links


@click.command()
@click.option('-c_span_search_url', help='The URL you get after searching on the c-span website', required=True,
              type=str)
@click.option('-load_more', default=True, type=bool,
              help='boolean of if the script should go through and load all videos on this search page')
@click.option('-is_save_to_one_file', required=True, type=bool,
              help='should all of the transcripts be outputted to one file or many individual files?')
@click.option('-add_video_name_to_file', required=True, type=bool,
              help='should the video file names be included in the file outputs')
def get_all_transcripts_for_search_term(c_span_search_url: str, add_video_name_to_file: bool, is_save_to_one_file: bool,
                                        load_more: bool = True):
    """
    Take any c-span search url (ex. https://www.c-span.org/search/?empty-date=1&sdate=&edate=&congressSelect=&yearSelect=&searchtype=Videos&sort=Best+Match&text=0&personid%5B%5D=34&formatid%5B%5D=55&show100=)
    preferably click on show 100, so this will run faster. The function will get all videos that come up on this
    search query and automatically retrive the cleaned transcripts for each of those videos.

    While this is running please do not interact with the browser this opens up.

    :param add_video_name_to_file: should the video file names be included in the file outputs
    :param is_save_to_one_file: should all of the transcripts be outputted to one file or many individual files?
    :param c_span_search_url: The url after searching on c-span's website. Make sure to select only videos.
    :param load_more: Boolean of if the script should try to load more on the page
    :return:
    """

    links = get_links_from_c_span_url(c_span_search_url, load_more)

    curr_video_index = 0
    total_videos = len(links)

    for video_link in links:
        # Let's be nice to c-span
        sleep(2)
        curr_video_index += 1
        video_name = video_link.split('/')[-1]
        print("transcribing video ({}/{}) {}".format(curr_video_index, total_videos, video_name))
        cleaned_transcript = transcipt_scraper(video_link)

        if is_save_to_one_file:
            with open("all_transcripts_concatenated.txt", "a") as f:
                if add_video_name_to_file:
                    f.write(video_name + "\n")
                f.write(cleaned_transcript)

        else:
            with open("{}.txt".format(video_name), "w") as f:
                if add_video_name_to_file:
                    f.write(video_name + "\n")
                f.write(cleaned_transcript)


if __name__ == '__main__':
    get_all_transcripts_for_search_term()
