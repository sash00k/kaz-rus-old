import re


def count_meaning_tokens(text: str) -> int:
    words = re.findall(r'(?u)\w+', str(text))
    count = len(words)
    for word in words:
        if re.findall(r'\b\d+\b', str(word)):
            count -= 1
    return count

def count_words_with_kz_symbols(text: str) -> int:
    kz_symbols = re.compile(r"\b(\w*["
                               u"\u04d8"u"\u04d9"
                               u"\u0492"u"\u0493"
                               u"\u049a"u"\u049b"
                               u"\u04a2"u"\u04a3"
                               u"\u04e8"u"\u04e9"
                               u"\u04b0"u"\u04b1"
                               u"\u04ae"u"\u04af"
                               u"\u04ba"u"\u04bb"
                               u"\u0406"u"\u0456"
                               r"]+\w*)+\b", flags=re.UNICODE)
    words = kz_symbols.findall(str(text))
    print('Pashok, sps, vse rabotaet!')
    return len(words)