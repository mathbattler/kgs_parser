import re
import requests
from bs4 import BeautifulSoup


def nick(string_to_search):  # возвращает ник игрока в строке из таблички
    result = re.split(r'"', str(string_to_search))[1]
    result_user = re.search(r'user=', str(result))
    begin_of_nickname = result_user.span()[1]
    nickname = result[begin_of_nickname:]
    return nickname


def link_of_sgf_file(string_with_http):
    # возвращает ссылку на sgf файл из таблички, если партия неприватная,
    # иначе возвращает None
    result = re.split(r'"', str(string_with_http))
    if (len(result) > 1):
        return str(result[1])
    else:
        return None  # это происходит, если партия приватная


def download_link(link):  # возвращает содержимое по ссылке link
    if link is None:
        return('')
    ufr = requests.get(link)
    return ufr.content


def kgs_game_parsing(nick1, nick2, tag):
    name = nick1
    url = 'http://www.gokgs.com/gameArchives.jsp?user=+' + name
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find_all('table')
    td_table = table[0].find_all('td')

    the_pair = sorted([nick1, nick2])

    # 0 -- ссылка на просмотр
    # 1 -- ник белого
    # 2 -- ник чёрного
    # 3 -- размер доски, фора
    # 4 -- дата и время начала партии
    # 5 -- тип партии (рейтинговая, свободная)
    # 6 -- результат (W+res, B+res,W+Time, B+14.5, ...)
    # всё происходит по модулю 7
    # n-ая строка это td_table[7(n-1)+x], где x от 0 до 6.

    l = len(td_table)
    n = l // 7
    for i in range(n):
        nick_w = nick(td_table[7 * i + 1])
        nick_b = nick(td_table[7 * i + 2])
        a_pair = sorted([nick_w, nick_b])
        link = link_of_sgf_file(td_table[7 * i])
        sgf = download_link(link).decode()
        finding_tag = re.search(tag, sgf)
        colour_of_winner = str(td_table[7 * i + 6])[4]
        if (finding_tag and (a_pair == the_pair)):
            return {'white': nick_w, 'black': nick_b,
                    'colour_of_winner': colour_of_winner, 'sgf': sgf}
    return None

# print(kgs_game_parsing('mathbatler', 'igoslave', 'Тестовый тег'))
