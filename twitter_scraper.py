from __future__ import print_function
from selenium import webdriver
from datetime import date, timedelta
import time
import logging
import argparse

log = logging.getLogger(__name__)


def scrape_loop(screen_name, since_date=date(2011, 4, 5), until_date=date.today(), delta_days=30, include_retweets=True,
                wait_secs=5):
    tweet_ids = set()
    for new_since_date, new_until_date in _next_dates(since_date, until_date, delta_days):
        new_tweet_ids = scrape(screen_name, new_since_date, new_until_date, include_retweets=include_retweets,
                               wait_secs=wait_secs)
        tweet_ids.update(new_tweet_ids)
        log.info("Found %s tweet ids for a total of %s unique tweet ids", len(new_tweet_ids), len(tweet_ids))
    return tweet_ids


def _next_dates(since_date, until_date, delta_days):
    last_date = False
    new_since_date = until_date
    while not last_date:
        new_until_date = new_since_date
        new_since_date = new_since_date - timedelta(days=delta_days)
        if new_since_date <= since_date:
            new_since_date = since_date
            last_date = True
        yield new_since_date, new_until_date


def scrape(screen_name, since_date, until_date, include_retweets=True, wait_secs=5):
    log.info("Scraping %s since %s until %s", screen_name, since_date, until_date)
    driver = webdriver.Chrome()
    try:
        driver.implicitly_wait(wait_secs)
        url = "https://twitter.com/search?q=from:{}+since:{}+until:{}".format(screen_name, since_date.isoformat(),
                                                                              until_date.isoformat())
        if include_retweets:
            url += "+include:retweets"
        log.debug("Getting %s", url)
        driver.get(url)

        scroll_count = 0
        last_tweet_count = 0
        while last_tweet_count != len(driver.find_elements_by_class_name("original-tweet")):
            scroll_count += 1
            last_tweet_count = len(driver.find_elements_by_class_name("original-tweet"))
            log.debug("Scrolling down %s. Found %s tweets.", scroll_count, last_tweet_count)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait_secs)

        return set([e.get_attribute("data-tweet-id") for e in driver.find_elements_by_class_name("original-tweet")])
    finally:
        driver.close()
        driver.quit()


def _to_date(date_str):
    date_split = date_str.split("-")
    return date(int(date_split[0]), int(date_split[1]), int(date_split[2]))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("screen_name")
    parser.add_argument("--since", default="2011-04-05", help="Tweets since this date. Default is 2011-04-05.")
    parser.add_argument("--until", default=date.today().isoformat(), help="Tweets until this date. Default is today.")
    parser.add_argument("--exclude-retweets", action="store_false")
    parser.add_argument("--delta-days", type=int, default=30, help="Number of days to include in each search.")
    parser.add_argument("--wait-secs", type=int, default=5, help="Number of seconds to wait between each scroll.")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger("selenium").setLevel(logging.WARNING)

    main_tweet_ids = scrape_loop(args.screen_name, _to_date(args.since), _to_date(args.until),
                                 include_retweets=args.exclude_retweets, delta_days=args.delta_days,
                                 wait_secs=args.wait_secs)
    for tweet_id in main_tweet_ids:
        print(tweet_id)
    log.info("Found %s unique tweet ids", len(main_tweet_ids))
