from utils import clean_text, divide_into_sentences, write_to_csv
from pathlib import Path
from parser import Parser

import pandas as pd
import time
import requests


class Group:
    def __init__(self, group_info: dict):
        self.domain: str = group_info['domain']
        self.owner_id: int = group_info['owner_id']
        self.group_type: str = group_info['group_type']
        self.need_comments: bool = group_info['need_comments']
        self.request_size: int = 100
        self.start_offset: int = 0

        self.path_to_file = Path('data', 'parts', self.domain + '.csv')
        self.file = None

    def _open_group_file(self):
        self.file = open(self.path_to_file)

    def _close_group_file(self):
        self.file.close()
        self.file = None

    def get_and_write_data(self, parser: Parser) -> None:
        self._open_group_file()
        write_to_csv.write_header(self)

        for req_num in range(10000):
            t_0 = time.perf_counter()
            response = requests.get('https://api.vk.com/method/wall.get',
                                    params={
                                        'owner_id': self.owner_id,
                                        'access_token': parser.get_token(),
                                        'v': parser.get_version(),
                                        'count': self.request_size,
                                        'offset': self.start_offset + req_num * self.request_size
                                    }).json()
            if 'error' in response:
                print('got error in response')
                continue
            try:
                posts = response['response']['items']
                if len(posts) == 0:
                    break
            except TypeError:
                print('got error while reading posts')
                continue

            texts = [post['text'] for post in posts]
            write_to_csv.write(self, texts, text_type='p')

            print('current post id in \"'+self.domain+'\" group:', posts[0]['id']+'; time -', round(time.perf_counter()-t_0,1))

            if self.need_comments:
                ids = [post['id'] for post in posts]
                self.get_and_write_comments(ids, parser)

        self._close_group_file()

    def get_and_write_comments(self, ids: list, parser: Parser):
        for cur_id in ids:
            response = requests.get('https://api.vk.com/method/wall.getComments',
                                    params={
                                        'owner_id': self.owner_id,
                                        'preview_length': 0,
                                        'post_id': cur_id,
                                        'access_token': parser.get_token(),
                                        'v': parser.get_version(),
                                        'count': self.request_size,
                                    }).json()
            if 'error' in response:
                continue
            try:
                comments = response['response']['items']
            except TypeError:
                print('got error while reading comments')
                continue

            texts = [comment['text'] for comment in comments]
            write_to_csv.write(self, texts, text_type='c')

    def read_data_from_file(self) -> pd.DataFrame:
        data = pd.read_csv(self.path_to_file, encoding='utf8', header=None, sep=',', on_bad_lines='skip')
        return data

    def clean_and_drop_short_ones(self):
        self._open_group_file()

        data = self.read_data_from_file()
        data['text'] = data['text'].apply(clean_text.clean)
        data.drop_duplicates(subset='text', inplace=True)

        divide_into_sentences.divide_text(self, data)
        del data

        self._close_group_file()
