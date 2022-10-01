import pandas as pd
import re
import time
import write_to_csv
from group import Group


def count_words(text: str) -> int:
    words = re.findall(r'(?u)\w+', str(text))
    count = len(words)
    for word in words:
        if re.findall(r'\b\d+\b', str(word)):
            count -= 1
    return count


def drop_short(data: pd.DataFrame) -> None:
    data['words_count'] = data['text'].apply(count_words)
    data.drop(data[data['words_count'] < 4].index, inplace=True)
    data.drop(columns=['words_count'], inplace=True)


def split(text: str) -> list:
    texts = re.split('\.', str(re.sub('[.?!]+', '.', text)))
    fin_texts = []
    for elem in texts:
        if bool(re.match('^\s*$', elem)):
            continue
        fin_texts.append(elem)
    return fin_texts


def divide_text(group: Group, data: pd.DataFrame) -> None:
    data['text'] = data['text'].apply(split)
    start_length = len(data)
    write_to_csv.write_header(group)
    t = time.time()
    print('Text dividing in', group.domain + ':')
    for i, row in data.iterrows():
        write_to_csv.write(group, row['text_type'], row['text'])
        if time.time() - t >= 1.0:
            t = time.time()
            print(round(i * 100 / start_length, 2), '%')
    print('100.00%')
