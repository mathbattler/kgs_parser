print ('I love Valera')
import re
import requests
from bs4 import BeautifulSoup


name = 'mathbatler'
url = 'http://www.gokgs.com/gameArchives.jsp?user=+' + name
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
#print(soup.prettify())

table=soup.find_all('table')
table0 = table[0]
td_table = table0.find_all('td')

#0 -- ссылка на просмотр
#1 -- ник белого
#2 -- ник чёрного
#3 -- размер доски, фора
#4 -- дата и время начала партии
#5 -- тип партии (рейтинговая, свободная)
#6 -- результат (W+res, B+res,W+Time, B+14.5, ...)
#всё происходит по модулю 7
#n-ая строка это td_table[7(n-1)+x], где x от 0 до 6.

l = len( td_table )
n = int (l/7)

#for i in range (0, n):
#    print (td_table[ 6+(i-1)*7])

#s = td_table[1]
#s2 = td_table[2]

def nick( string_to_search ): #возвращает ник игрока в строке из таблички
    result = re.split(r'"', str(string_to_search))
    result = result[1]
    result_user = re.search(r'user=', str(result))
    begin_of_nickname = result_user.span()[1]
    nickname = result[begin_of_nickname : ]
    return nickname

#print ( nick( s ), nick( s2 ) )

def link_of_sgf_file( string_with_http ): #возвращает ссылку на sgf файл из таблички, если партия неприватная, иначе возвращает None
        result = re.split(r'"', str(string_with_http))
        if (len(result) > 1):
            link = str( result[1] )
        else:
             link = None #это происходит, если партия приватная
        return link

#link = link_of_sgf_file(td_table[7])

#print ( link )

def download_link( link ):
    if (link == None):
        return( '' )
    f=open(r'1.sgf',"wb") #открываем файл для записи, в режиме wb
    ufr = requests.get(str(link)) #делаем запрос
    #f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    #f.close()
    #f=open(r'1.sgf',"r")
    #s = f.read()
    #f.close()
    #return s
    return ufr

tag = 'Тестовый тег'
#result = re.search(tag, str(s) )


for i in range (n):
    nick_w = nick( td_table[7*i + 1] )
    nick_b = nick( td_table[7*i + 2] )
    link = link_of_sgf_file(td_table[7*i])
    sgf = download_link( link )
    finding_tag = re.search(tag, str(sgf) )
    colour_of_winner = str(td_table[7*i+6])[4]

    if (colour_of_winner == 'W'):
        winner = nick_w
    else:
        winner = nick_b

    if (finding_tag):
        finding = 'tag_yes'
    else:
        finding = 'tag_no'
    print (nick_w +' vs '+ nick_b, finding, winner, 'won')
