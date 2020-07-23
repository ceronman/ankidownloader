import logging
import pathlib
import sys
import urllib

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


def translate_words(driver):
    i = 200
    with open("words3.txt", encoding="utf-8") as words_file:
        for line in words_file:
            if not line:
                continue
            word = line.strip()
            translations = translate_word(driver, word)
            translations = ", ".join(repr(t) for t in translations)
            print(f"{word};{translations}")
            download_speech(word)
            i = i - 1
            if i < 0:
                break

def translate_word(driver, word):
    logging.debug("translating %s", word)
    if word.startswith("het "):
        query = word.replace("het ", "", 1)
    elif word.startswith("de "):
        query = word.replace("de ", "", 1)
    else:
        query = word
    query = urllib.parse.quote(query)
    logging.debug("translation query: %s", query)
    url = f"https://www.interglot.nl/woordenboek/nl/es/zoek?q={query}"
    logging.debug("Querying %s", url)
    driver.get(url)
    try:
        element = driver.find_element_by_class_name("defTransList")
    except NoSuchElementException:
        logging.warning("Translation not found for " + word)
        return []
    translations = element.find_elements_by_tag_name("a")
    return [t.text for t in translations][:4]


def download_speech(word):
    logging.debug("downloading sound for %s", word)
    data = {"msg": word, "lang": "Ruben", "source": "ttsmp3"}
    response = requests.post("https://ttsmp3.com/makemp3_new.php", data=data)
    response = response.json()
    sound_url = response["URL"]
    logging.debug("sound url: %s", sound_url)
    sound_response = requests.get(sound_url)
    filename = word.replace(" ", "_") + ".mp3"
    filepath = pathlib.Path("sounds", filename)
    filepath.parent.mkdir(exist_ok=True)

    with filepath.open(mode="wb") as file:
        file.write(sound_response.content)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.debug("Testing the logger")
    options = Options()
    options.binary_location = "/usr/bin/chromium-freeworld"
    options.headless = True
    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 10)
        translate_words(driver)