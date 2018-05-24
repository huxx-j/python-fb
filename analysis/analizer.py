import json
import re
from collections import Counter

from konlpy.tag import Twitter


# json 파일평, key 값을 주면 문자열을 리턴한다
def json_to_str(filename, key):
    jsonfile = open(filename, 'r', encoding='utf-8')
    json_string = jsonfile.read()
    json_data = json.loads(json_string)

    data = ''

    for item in json_data:
        value = item.get(key)

        data += re.sub(r'[^\w]', '', value)

    return data


# 명사를 추출해서 빈도수를 알려줌
def count_wordfreq(data):
    twitter = Twitter()
    nouns = twitter.nouns(data)
    count = Counter(nouns)

    return count


# datastring = json_to_str("/Users/huxx_j/Downloads/ex/chosun.json", "message_str")
# print(datastring)
#
# count_wordfreq(datastring)
