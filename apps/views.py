# -*- coding: utf-8 -*-
__author__ = 'pilgrim'
from coffin.views.generic.base import TemplateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect, HttpResponse
from forms import *
import urllib2
import datetime
import lxml.html

from models import *
from lenta import *
import time


# class CronTab(object):
#     def __init__(self, *events):
#         self.events = events
#
#     def run(self):
#         t=datetime.datetime.now().timetuple()[:5]
#         while 1:
#             for e in self.events:
#                 e.check(t)
#
#             t += datetime.timedelta(minutes=1)
#             while datetime.datetime.now() < t:
#                 time.sleep((t - datetime.datetime.now()).seconds)


class MyPageView(TemplateView):
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        return context



class OurNews(TemplateView):
    template_name = 'our_news.html'

    def get_context_data(self, **kwargs):
        context = super(OurNews, self).get_context_data(**kwargs)
        # context['current_time'] = str(datetime.datetime.now().day) + '/' + str(datetime.datetime.now().month) + '/' +\
        #                 str(datetime.datetime.now().year) + ' ' + str(datetime.datetime.now().hour) + ':' + \
        #                 str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second) + str(' msk')
        context['records'] = New.objects.all().order_by('-date')[:3]
        dd = datetime.datetime.now().day
        mm = datetime.datetime.now().month
        yyyy = datetime.datetime.now().year
        if dd < 10:
                dd = '0' + str(dd)
        if mm < 10:
                mm = '0' + str(mm)
        context['dd'] = dd
        context['mm'] = mm
        context['yyyy'] = yyyy



        # context['tt'] = int(time.mktime(time.strptime('2000-01-01 12:34:00', '%Y-%m-%d %H:%M:%S')))
        return context

    def post(self, request):
        MY_DEBUG = False
        if request.POST:
            dd = datetime.datetime.now().day
            mm = datetime.datetime.now().month
            yyyy = datetime.datetime.now().year
            if dd < 10:
                dd = '0' + str(dd)
            if mm < 10:
                mm = '0' + str(mm)
            # формируем сегодняшний урл со списком новостей
            today_link = 'http://lenta.ru/news/' + str(yyyy) + '/' + str(mm) + '/' + str(dd) + '/'
            # today_link = 'http://lenta.ru/news/2014/07/25'
            # открываем
            try:
                response = urllib2.urlopen(today_link)
            except:
                print 'no url'
            if response.getcode() == 200:
                data = response.read()
                # headers = response.info()

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
            counter = 0
            all_records = []
            for new_url in massiv_of_pages:
                counter += 1
                if MY_DEBUG:
                    if counter == 6:
                        print 'process stopped in 5 iter because of debug mode. set up debug on false to parse all'
                        break
                try:
                    new_response = urllib2.urlopen(new_url)
                except:
                    print 'couldnt open. sorry'
                if new_response.getcode() == 200:
                    one_record = []
                    page = new_response.read()
                    print counter, 'URL: ', new_url

                    # тащим картинки
                    """
                    img_date_link = 'src="http://icdn.lenta.ru/images/' + str(yyyy) +'/' + str(mm) + '/' + str(dd) + '/'
                    if img_date_link in page:
                        s = page.index(img_date_link)
                        image_url = page[s+5:s+105]
                        try:
                            open_image = urllib2.urlopen(image_url)
                            print open_image
                            #  протестить и настроить
                            # out = open("/gallery/img1.jpg", 'wb')
                            # out.write(open_image.read())
                            # out.close()
                            #
                        except:
                            print 'couldnt open. sorry'
                    """

                    if '<title>' in page:
                        start_title = page.index('<title>')
                        end_title = page.index('</title>')
                        title = page[start_title:end_title]
                        num_of_title_word = 0
                        for i in title.split(' '):
                            num_of_title_word += 1
                            if num_of_title_word == 2:
                                if i == 'Из':
                                    category = 'Из жизни'
                                elif i == 'Бывший':
                                    category = 'Бывший СССР'
                                elif i == 'Интернет':
                                    category = 'Интернет и СМИ'
                                elif i == 'Наука':
                                    category = 'Наука и техника'
                                else:
                                    category = i[:-1]
                                one_record.append(category)
                    # s = 'id=\"comments-count\"'
                    # if s in page:
                    #     print 'comments found!', page.index(s)
                    #     print page[page.index(s)+20:page.index(s)+25]
                    dom = lxml.html.document_fromstring(page.decode("utf-8"))
                    quantity_of_articles = 0

                    length_of_string = 0
                    NORMAL_LENGTH_OF_STRING = 80

                    url = new_url
                    one_record.append(url)

                    for j in dom.cssselect("div.b-topic__header h1"):  # headers
                        header = j.text.encode("utf-8")
                        one_record.append(header)

                    nomer_slova = 0
                    # for x in dom.cssselect("div.b-text p"):  # articles
                    for x in dom.cssselect("div.b-text p"):
                        if x.text is not None:  # иногда почему-то x бывает None
                            words = x.text.split()

                        for word in words:
                            nomer_slova += 1
                            if nomer_slova == 1:
                                one_record.append(unicode(word).encode('utf-8') + ' ')
                            else:
                                one_record[3] += unicode(word).encode('utf-8') + ' '

                            # выравнивание текста до 80 символов
                            length_of_string += len(word)
                            if length_of_string > NORMAL_LENGTH_OF_STRING:
                                one_record[3] += ''
                                length_of_string = 0

                        # содание нового абзаца у себя, если он есть у донора
                        if 0x0a or 0x0d:  # if new line
                            one_record[3] += "\n\n"
                            length_of_string = 0
                all_records.append(one_record)
            all_base = New.objects.all()
            a = []
            for i in all_base:
                a.append(i.url)  # смотрю какие страницы в базе уже есть
            qty_of_new = 0
            for record in all_records:
                if record[1] not in a:  # добавляю только те, которых у меня еще нет (новые)
                    New.objects.create(source='lenta.ru',
                                       url=record[1],
                                       date=datetime.datetime.now(),
                                       category=record[0],
                                       header=record[2],
                                       text=record[3])
                    qty_of_new += 1

            print 'updated', qty_of_new, 'news'
            return HttpResponseRedirect('/')


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        slug = self.kwargs['article']
        for rec in New.objects.all():
            if slug in rec.url:
                context['article'] = rec
        return context


class AllNewsView(TemplateView):
    template_name = 'allnews.html'

    def get_context_data(self, **kwargs):
        context = super(AllNewsView, self).get_context_data(**kwargs)
        curr_year = self.kwargs.values()[0]
        curr_day = self.kwargs.values()[1]
        curr_month = self.kwargs.values()[2]
        articles = []
        for rec in New.objects.all():
            if curr_year in str(rec.date) and curr_month in str(rec.date) and curr_day in str(rec.date):
                articles.append(rec)
        context['articles'] = articles
        return context