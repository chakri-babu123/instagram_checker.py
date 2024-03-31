#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from termcolor import colored
import random
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_usernames(username, num_usernames=20, delay_min=1, delay_max=3):
    url = f"https://www.instagram.com/{username}/"
    try:
        delay = random.uniform(delay_min, delay_max)
        time.sleep(delay)
        logging.info(f"Fetching Instagram profile: {username}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        usernames = set()
        for suggestion in soup.find_all('a', {'class': 'FPmhX notranslate _0imsa '}):
            suggestion_username = suggestion.text
            if suggestion_username.lower().startswith(username.lower()):
                usernames.add(suggestion_username)
            if len(usernames) >= num_usernames:
                break
        logging.info(f"Scraped {len(usernames)} similar usernames")
        return list(usernames)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Instagram profile: {e}")
        return []

def check_passwords(usernames, passwords):
    matched = False
    for username in usernames:
        delay = random.uniform(1, 3)
        time.sleep(delay)
        if username in passwords:
            print(colored(f"{username}: {username} - Matched", 'green'))
            matched = True
        else:
            print(colored(f"{username} - Not matched", 'red'))
    return matched

def main():
    username = input("Enter Instagram username: ")
    password1 = input("Enter password 1: ")
    password2 = input("Enter password 2: ")
    password3 = input("Enter password 3: ")
    passwords = [password1, password2, password3]

    num_usernames = int(input("Enter number of usernames to scrape (default is 20): ") or 20)
    delay_min = float(input("Enter minimum delay between requests in seconds (default is 1): ") or 1)
    delay_max = float(input("Enter maximum delay between requests in seconds (default is 3): ") or 3)

    logging.info("Starting Instagram username scraping and password checking")

    usernames = scrape_usernames(username, num_usernames, delay_min, delay_max)

    if usernames:
        logging.info("Starting password checking")
        matched = check_passwords(usernames, passwords)

        if not matched:
            print(colored("No matches found for any username-password pair.", 'red'))
    else:
        print(colored("Exiting due to error.", 'red'))

if __name__ == "__main__":
    main()
