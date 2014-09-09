# -*- coding: utf-8 -*-
__author__ = 'pilgrim'
import urllib2
import datetime
import lxml.html

def lenta():
    my_file = open('file.txt', 'w')
    # определяем сегодняшнюю дату
    dd = datetime.datetime.now().day
    mm = datetime.datetime.now().month
    yyyy = datetime.datetime.now().year
    if dd < 10:
        dd = '0' + str(dd)
    if mm < 10:
        mm = '0' + str(mm)
    # формируем сегодняшний урл со списком новостей
    today_link = 'http://lenta.ru/news/' + str(yyyy) + '/' + str(mm) + '/' + str(dd) + '/'
    # открываем
    try:
        response = urllib2.urlopen(today_link)
    except:
        print 'no url'
    if response.getcode() == 200:
        data = response.read()
        headers = response.info()

        # собираем ссылки на сегодняшние статьи (новости)
        massiv_of_pages = []
        for word in data.split(' '):
            link = 'href=\"/news/' + str(yyyy) + '/' + str(mm) + '/' + str(dd)
            if link in word:
                word = word[6:]
                word = word[:word.index('\"')]
                word = 'http://lenta.ru' + word
                if word not in massiv_of_pages:
                    massiv_of_pages.append(word)  # массив новых урлов готов

    # работа на новых страницах
    qq=0
    counter = 0
    for new_url in massiv_of_pages:
        counter += 1
        try:
            new_response = urllib2.urlopen(new_url)
        except:
            print 'couldnt open. sorry'
        if new_response.getcode() == 200:
            page = new_response.read()
            print counter, 'URL: ', new_url
            if '<title>' in page:
                start_title = page.index('<title>')
                end_title = page.index('</title>')
                title = page[start_title:end_title]
                num_of_title_word = 0
                for i in title.split(' '):
                    num_of_title_word += 1
                    if num_of_title_word == 2:
                        if i == 'Из':
                            print>>my_file, 'Из жизни'
                        elif i == 'Бывший':
                            print>>my_file, 'Бывший СССР'
                        elif i == 'Интернет':
                            print>>my_file, 'Интернет и СМИ'
                        elif i == 'Наука':
                            print>>my_file, 'Наука и техника'
                        else:
                            print>>my_file, i
            dom = lxml.html.document_fromstring(page.decode("utf-8"))
            quantity_of_articles = 0
            length_of_string = 0
            NORMAL_LENGTH_OF_STRING = 80

            print>>my_file, 'ИСТОЧНИК: ', new_url
            for j in dom.cssselect("div.b-topic__header h1"):  # headers
                print>>my_file, 'ТЕМА:', j.text.encode("utf-8"), "\n"
            print>>my_file, 'СТАТЬЯ: '
            for x in dom.cssselect("div.b-text p"):  # articles
                if x.text is not None:  # kostyl. inogda x byvaet none pochemy-to
                    words = x.text.split()
                for word in words:
                    length_of_string += len(word)
                    if length_of_string > NORMAL_LENGTH_OF_STRING:
                        print>>my_file, ""
                        length_of_string = 0
                    if word != '<a':
                        print>>my_file, word.encode('utf-8'),
                if 0x0a or 0x0d:  # if new line
                    print>>my_file, "\n"
                    length_of_string = 0
                quantity_of_articles += 1


                # print '**** links ****'
                # for i in dom.cssselect("div.b-text p > a"):  # links
                #   if i.attrib.get("href"):
                #     print '[', i.text.encode('utf-8'), ']', '[', i.attrib.get("href").encode('utf-8'), ']'
                #
                # print "\n", "quantity of articles:", quantity_of_articles
        qq += quantity_of_articles
    print qq
    print>>my_file, 'that is all for now...'

    return my_file