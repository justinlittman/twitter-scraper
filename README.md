# twitter-scraper

A tool for scraping tweet ids from the Twitter website.

## Explanation
Tweets collected from Twitter's APIs provide metadata about
the tweets that is machine-readable (in JSON) and may not be available from
the website. For the purposes of archiving and/or analyzing tweets
this metadata is potentially significant.

Unfortunately, Twitter's APIs don't support getting a comprehensive
set of a user's tweets. Twitter's [statuses/user_timeline](https://dev.twitter.com/rest/reference/get/statuses/user_timeline)
REST API method only allows collecting the last 3,200 tweets. Similarly,
Twitter's [Search API](https://dev.twitter.com/rest/public/search) will
only provide tweets from the last 6-9 days.

twitter-scraper attempts to support getting a comprehensive set of a
user's tweets (with optional date constraints). It accomplishes this 
by making requests to Twitter's
website search (which is different than the Search API) and
extracting tweet ids. These tweet ids can then be passed to
[twarc](https://github.com/edsu/twarc) to retrieve from Twitter's REST
API (aka "hydrating").

## Installation
1. Install Python, Pip, Git, and Chrome.
2. Clone this repo: `git clone https://github.com/justinlittman/twitter-scraper.git`
3. Install [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/). 
   On a Mac, this can be done with `brew install chromedriver`. On Ubuntu:
   
        wget http://chromedriver.storage.googleapis.com/2.24/chromedriver_linux64.zip
        unzip chromedriver_linux64.zip
        sudo mv chromedriver /usr/bin/
              
4. Install Selenium: `pip install selenium`
5. Install Twarc: `pip install twarc`

## Usage

        python twitter_scraper.py -h
        usage: twitter_scraper.py [-h] [--since SINCE] [--until UNTIL]
                                  [--exclude-retweets] [--delta-days DELTA_DAYS]
                                  [--wait-secs WAIT_SECS] [--debug]
                                  screen_name
        
        positional arguments:
          screen_name
        
        optional arguments:
          -h, --help            show this help message and exit
          --since SINCE         Tweets since this date. Default is 2011-04-05.
          --until UNTIL         Tweets until this date. Default is today.
          --exclude-retweets
          --delta-days DELTA_DAYS
                                Number of days to include in each search.
          --wait-secs WAIT_SECS
                                Number of seconds to wait between each scroll.
          --debug

## Running
To collect @realDonaldTrump's tweets between January 1, 2016 and April 1, 2016:

1. Run twitter_scraper and write the tweet ids to a file.

   *Leave your system alone while twitter_scraper is running.* I received 
   inconsistent results while I was doing other work on my system while 
   twitter_scraper was running. Better yet, use a VM.
   
   *Tip*: You can get the date that a user joined Twitter from the user's
   account page.
   
   *Tip*: Timestamp the tweet id file by using ` > tweet_ids_$(date -d "today" +"%Y%m%d%H%M").txt`
   
        python twitter_scraper.py @realDonaldTrump --since=2016-01-01 --until=2016-04-01 > tweet_ids.txt

2. Hydrate the tweet ids with Twarc and write to a file. *You will need to
   provide Twarc with a set of Twitter API keys.* For more information,
   see [Twarc's documentation](https://github.com/edsu/twarc#twitter-api-keys).

        twarc.py --hydrate tweet_ids.txt > tweets.json

## Acknowledgements
This work was inspired by the [Trump Twitter Archive](http://www.trumptwitterarchive.com/).

And appreciative (once again) for Ed Summer's [twarc](https://github.com/edsu/twarc).
