import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import os
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

class ParseUrl:

	def __init__(self):
		"""
		Performs parsing of the html for the url provided and saves results into jsonl file
		"""


		self.base_url = os.getenv("INPUT_URL")
		self.output = os.getenv("OUTPUT_FILE")
		self.proxy = os.getenv("PROXY")
		self.next_url = "/page/1"
		self.results = []

	def _perform_parsing(self):
		"""
		Performs parsing of the html for the url provided
		"""

		i=1
		while self.next_url:
			session = webdriver.Chrome()
			session.get(f"{self.base_url}/page/{i}")
			sleep(15)
			soup = BeautifulSoup(session.page_source, "html.parser")
			quotes = soup.find_all(class_="quote")

			for quote in quotes:
				text = quote.select_one(".text").get_text()
				author = quote.select_one(".author").get_text()
				tags = [tag.get_text() for tag in quote.select(".tag")]
				self.results.append({"text": text, "by": author, "tags": tags})

			self.next_url = BeautifulSoup(session.page_source, 'html.parser').select_one('.next a')
			i=i+1
		session.quit()

	def save_to_file(self):
		"""
		Saves parsed list of dictionaries into jsonl file
		"""

		with open(self.output, "w") as file:
			for result in self.results:
				file.write(json.dumps(result) + "\n")

	def perform(self):
		self._perform_parsing()
		self.save_to_file()

