import requests
from bs4 import BeautifulSoup


class RandomBird:
    def __init__(self):
        self.bird_url = "https://ebird.org/species/surprise-me"
        bird_page = requests.get(self.bird_url)
        bird_soup = BeautifulSoup(bird_page.content, "html.parser")

        bird_titles = bird_soup.findAll("title")
        bird_image = bird_soup.find("img", class_="ImageResponsive")
        self.main_image = bird_image['data-src']

        bird_title = str(bird_titles[0])
        title_len = len(bird_title)
        self.bird_name = bird_title[7:title_len-16]
