import re
import count_words


def clean_short_texts(text, min_count_of_meaning_words):
    count = count_words.count_meaning_tokens(text)
    return text if count >= min_count_of_meaning_words else ''

def remove_hashtags(text: str) -> str:
    return re.sub(r'\b#\w+\b', '', str(text))

def remove_vk_specials(text: str) -> str:
    return re.sub(r'[(club\d+\b)(id\d+\b)]+','', str(text))

def remove_urls(text: str) -> str:
    text = re.sub(r'\b\w+\.\w+\b','', str(text)) #like 'SITE.KZ'
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', str(text))
    text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', str(text))
    return text

def remove_emoji(text: str) -> str:
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002500-\U00002BEF"
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_normal_symbols(text: str) -> str:
    return re.sub(r'[&~`$%^\*)(+=\]\[{}|\\/#_~<>"@«»\n“”‘’\'\'\"\"\s]+',' ', str(text))

def remove_admin_anon(text: str) -> str:
    text = re.sub(r'[(админ)(не анон)(анон)]', '', str(text), flags=re.I)
    return text

def remove_numbers(text: str) -> str:
    return re.sub(r'(\d){3,11}','', str(text))

def clean(text: str) -> str:
    text = remove_vk_specials(text)
    text = remove_urls(text)
    text = remove_emoji(text)
    text = remove_normal_symbols(text)
    text = remove_numbers(text)
    return text

def light_clean(text: str) -> str:
    return re.sub(r'[\n]+', ' ', str(text))
