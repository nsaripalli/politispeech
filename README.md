# 2020 Democratic Candidates Political Speech Generator

This is a website to generate political canidate speeches using Open AI's GPt-2. It runs on top of gpt-2 cloud run. The model training was done from speeches found on cspan for each canidates via the text transcripts. The backend runs on google cloud run. If you would like to learn how the infastructure works please look at https://github.com/minimaxir/gpt-2-cloud-run.

## C-span Scraping
Under mining the code to scrape cspan videos for the transcrips can be found:
 STEPS TO RUN PROGRAM:

* Install all packages `pip3 install -r requirements.txt`
* cd into the `mining` folder to run the transcript_scraper
* run `python3 transcript_scraper.py` with the specified arguments

To see what arguments need to be passed in, type in python transcript_scraper.py --help 

To get a url for the c_span_search_url input:
1. Go to C-SPAN's main website and search for a term, then click on the videos button just under the search bar to only get video results.
2. Include any filters you want in the search
3. (Optional) Click on show 100 next to `showing 1-N` on the right of videos sorted by
4. Copy and paste your full url (with the www) in the browser into the program 

If all videos are to be concated into one file, the file name will show up as `all_transcripts_concatenated.txt`
Otherwise each file name will be speech name

example `python3 transcript_scraper.py -c_span_search_url https://www.c-span.org/search/\?empty-date\=1\&sdate\=\&edate\=\&congressSelect\=\&yearSelect\=\&searchtype\=Videos\&sort\=Best+Match\&text\=0\&personid%5B%5D\=34\&formatid%5B%5D\=55\&show100\= -is_save_to_one_file True -add_video_name_to_file False`

NOTE: If you want to download just one video's transcript you can you the function transcipt_scraper in here and just
give it the video's url
