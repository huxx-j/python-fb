import json

import requests
from datetime import datetime, timedelta

BASE_URL_FB_API = "https://graph.facebook.com/v3.0"
ACCESS_TOKEN = "EAACEdEose0cBABkFBiQJBWZC13Me5jeXN70K5TNbdlEXxCDZCpZA7nOoPpNUBEnMWVKplw6wccKgIL0FOatdCDiHpBQ1pNs02BoQGXnRLT1yy5kEvb6FPGXGOzcdIiVqOZAWUsDLL1UfIjuZCZAaybXQOUkZCv5ZAZB5whZC31nckKr263efRJgR10tUXVp7847K3Rei4DXwJTPwZDZD"
LIMIT_REQUEST = 10
pagename = "jtbcnews"
from_date = "2018-05-20"
to_date = "2018-05-23"


def get_json_result(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    except Exception as e:
        return "%s : Error For Request [%s]" % (datetime.now(), url)


# 페이지 네임을 주면 페이지의 id를 리턴한다.

def fb_name_to_id(pagename):
    base = BASE_URL_FB_API
    node = "/%s" % pagename
    params = "/?access_token=%s" % ACCESS_TOKEN
    url = base + node + params
    json_result = get_json_result(url)

    return json_result["id"]


# 페이스북 페이지네임, 시작날짜, 끝날짜를 주면 json 형태로 데이타를 리턴해준다.

def fb_get_post_list(pagename, from_date, to_date):
    page_id = fb_name_to_id(pagename)
    base = BASE_URL_FB_API
    node = "/%s/posts" % page_id
    fields = "/?fields=id,message,link,name,type,shares,created_time,comments.limit(0).summary(true),reactions.limit(0).summary(true)"
    duration = "&since=%s&until=%s" % (from_date, to_date)
    parameters = "&limit=%s&access_token=%s" % (LIMIT_REQUEST, ACCESS_TOKEN)

    url = base + node + fields + duration + parameters
    c = 1
    isNext = True
    postList = []
    while isNext:
        tmpPostList = get_json_result(url)
        for post in tmpPostList["data"]:
            postVo = preprocess_post(post)
            postList.append(postVo)
            c += 1

        paging = tmpPostList.get("paging").get("next")

        if paging != None:
            url = paging
        else:
            isNext = False

    print("{0}개 포스트를 가져왔습니다.".format(c))

    # save results to file
    with open("/Users/huxx_j/Downloads/ex/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

    # return postList


def preprocess_post(post):
    # 작성일 +9시간 해줘야함
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

    # 쉐어수
    if "shares" not in post:
        shares_count = 0
    else:
        shares_count = post["shares"]["count"]

    # 리액션
    if "reactions" not in post:
        reactions_count = 0
    else:
        reactions_count = post["reactions"]["summary"]["total_count"]

    # 댓글수
    if "comments" not in post:
        comments_count = 0
    else:
        comments_count = post["comments"]["summary"]["total_count"]

    # 메세지 수
    if "message" not in post:
        message_str = ""
    else:
        message_str = post["message"]

    postVo = {

        "shares_count": shares_count,

        "reactions_count": reactions_count,

        "comments_count": comments_count,

        "message_str": message_str,

        "created_time": created_time

    }

    return postVo


# fb_get_post_list(pagename, from_date, to_date)

# url = 'http://192.168.1.14:8088/mysite4/api/gb/list2'
#
# result = get_jasom_result(url)
# print(result)
