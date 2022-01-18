import logging
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import InvalidSchema


class Page():
    def __init__(self, url: str, line_width: int, img: bool):
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.domain = urlparse(self.url).hostname
        self.line_width = line_width
        self.image_filter = img
        self.document_path = f'{Path(__file__).resolve().parent.parent}/files/{self.domain}.txt'

    def get_useful_content(self):
        its_url = self._validate()
        print(its_url)
        if not its_url:
            self.logger.info(f'Адрес:"{self.url}" является некорректным.')
            return False
        else:
            page_data: dict = self._parse()
            self._create_document(page_data=page_data)
            return True

    def _validate(self) -> bool:
        try:
            if requests.get(self.url).status_code == 200:
                return True
            return False
        except InvalidSchema:
            return False

    def _parse(self) -> dict:
        page_data = dict()
        page = requests.get(self.url).text
        soup = BeautifulSoup(page)
        headline = soup.find('h1').get_text()
        if self.image_filter:
            p_tags = soup.find_all(['p', 'img'])
        p_tags = soup.find_all('p')
        p_tags_text = [tag.get_text().strip() for tag in p_tags]
        sentence_list = [sentence for sentence in p_tags_text if '\n' not in sentence]
        sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
        article = ' '.join(sentence_list)
        page_data['headline'] = headline
        page_data['article'] = article

        return page_data

    def _create_document(self, page_data: dict) -> None:
        document = open(self.document_path, 'w')
        document.write(page_data['headline'] + '\n')
        article = list()
        start = 0
        end: int = self.line_width
        for i in range(int(len(page_data['article']) / self.line_width)):
            if len(page_data['article']) <= end:
                line = page_data['article'][start:(len(article) - 1)]
                article.append(line)
                break
            while page_data['article'][end] not in [' ', ',', '.']:
                end -= 1
            line = page_data['article'][start:(end + 1)] + '\n'
            article.append(line)
            start = end + 1
            end += self.line_width + 1
        for article_line in article:
            document.write(article_line)
        document.close()
