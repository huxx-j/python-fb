import webbrowser

import matplotlib.pyplot as plt
import pytagcloud as pytagcloud
from matplotlib import font_manager


# matplotlib 그래프


def show_gragh_bar(dict_word, pagename):
    # 한글처리
    font_filename = '/Library/Fonts/Arial Unicode.ttf'
    font_name = font_manager.FontProperties(fname=font_filename).get_name()
    plt.rc('font', family=font_name)

    # 라벨처리
    plt.xlabel("주요단어")
    plt.ylabel("빈도수")
    plt.grid(True)

    # 데이터 대입
    dict_keys = dict_word.keys()
    dict_values = dict_word.values()
    plt.bar(range(len(dict_word)), dict_values, align='center')
    plt.xticks(range(len(dict_word)), list(dict_keys), rotation=70)

    save_filename = "/Users/huxx_j/Downloads/ex/%s_bar_gragh.png" % pagename
    plt.savefig(save_filename, bbox_inches='tight')

    plt.show()


# 워드 클라이드
def word_cloud(dict_word, pagename):
    taglist = pytagcloud.make_tags(dict_word.items(), maxsize=80)
    save_filename = "/Users/huxx_j/Downloads/ex/%s_word_cloud.jpg" % pagename
    pytagcloud.create_tag_image(
        taglist,
        save_filename,
        size=(800,600),
        fontname="korean",
        rectangular=False
    )

    webbrowser.open(save_filename)

