# -*- coding: utf-8 -*-
__author__ = 'pilgrim'
from coffin.views.generic.base import TemplateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect, HttpResponse
from forms import *
import urllib2
import lxml.html
from django.utils import timezone  # во всем проекте поменял datetime.datetime на timezone
from models import *
from lenta import *
import time
from .libs import download_file
import os


class MyPageView(TemplateView):
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        return context


class OurNews(TemplateView):
    template_name = 'our_news.html'

    def get_context_data(self, **kwargs):
        context = super(OurNews, self).get_context_data(**kwargs)
        qty_of_news = 3  # количество новостей на главной
        context['records'] = New.objects.all().order_by('-date')[:qty_of_news]
        context['image'] = New.objects.order_by('-id')[0:1].get().img1
        context['image_next'] = New.objects.order_by('-id')[1:2].get().img1

        dd = timezone.now().day
        mm = timezone.now().month
        yyyy = timezone.now().year

        if dd < 10:
                dd = '0' + str(dd)
        if mm < 10:
                mm = '0' + str(mm)

        context['dd'] = dd
        context['mm'] = mm
        context['yyyy'] = yyyy

        return context

    def post(self, request):
        MY_DEBUG = False
        if request.POST:
            dd = timezone.now().day
            mm = timezone.now().month
            yyyy = timezone.now().year
            if dd < 10:
                dd = '0' + str(dd)
            if mm < 10:
                mm = '0' + str(mm)
            # формируем сегодняшний урл со списком новостей
            today_link = 'http://lenta.ru/news/' + str(yyyy) + '/' + str(mm) + '/' + str(dd) + '/'

            try:
                response = urllib2.urlopen(today_link)  # открываем
            except:
                print 'no url'
            massiv_of_pages = []
            if response.getcode() == 200:
                data = response.read()

                for word in data.split(' '):  # собираем ссылки на сегодняшние статьи (новости)
                    link = 'href=\"/news/' + str(yyyy) + '/' + str(mm) + '/' + str(dd)
                    if link in word:
                        word = word[6:]
                        word = word[:word.index('\"')]
                        word = 'http://lenta.ru' + word
                        if word not in massiv_of_pages:
                            massiv_of_pages.append(word)  # массив новых урлов готов

            # работа на новых страницах
            counter = 0
            qty_of_new = 0
            miss = 0
            db_news = [new.url for new in New.objects.all()]
            for new_url in massiv_of_pages:
                if new_url in db_news:
                    # Если новость уже есть - не парсим!
                    miss += 1
                    continue
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

                    if '<title>' in page:  # парсим заголовок
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
                    dom = lxml.html.document_fromstring(page.decode("utf-8"))

                    url = new_url
                    one_record.append(url)

                    for j in dom.cssselect("div.b-topic__header h1"):  # headers
                        header = j.text.encode("utf-8")
                        one_record.append(header)

                    nomer_slova = 0
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
                            # length_of_string = 0
                            # NORMAL_LENGTH_OF_STRING = 80
                            # length_of_string += len(word)
                            # if length_of_string > NORMAL_LENGTH_OF_STRING:
                            #     one_record[3] += ''
                            #     length_of_string = 0

                        # содание нового абзаца у себя, если он есть у донора
                        if 0x0a or 0x0d:  # if new line
                            one_record[3] += "\n\n"
                            length_of_string = 0
                    # Сохраняем новость (без картинки)
                    new = New.objects.create(source='lenta.ru',
                                             url=one_record[1],
                                             date=timezone.now(),
                                             category=one_record[0],
                                             header=one_record[2],
                                             text=one_record[3])
                    new.save()
                    qty_of_new += 1

                    # парсим картинку
                    flag = 'http://icdn.lenta.ru/images/' + str(yyyy) + '/' + str(mm) + '/' + str(dd) + '/'
                    if flag in page:
                        start_img_url = page.index(flag)
                        end_img_url = start_img_url + 100
                        img_url = page[start_img_url:end_img_url]
                        try:
                            new_page_with_img = urllib2.urlopen(img_url)
                            if new_page_with_img.getcode() == 200:
                                # Заружаем и Добавляем картинку в нашу новость
                                download_file(new, 'img1', url=img_url, save=True)
                        except:
                            print 'couldn\'t open image'

            # Судя по всему уже ненужно:

                # all_records.append(one_record)
            # закончили парсить. сейвим
            # all_base = New.objects.all()
            # a = []
            # for i in all_base:
            #     a.append(i.url)  # смотрю какие страницы в базе уже есть
            # for record in all_records:
            #     print record[5]
            #     if record[1] not in a:  # добавляю только те, которых у меня еще нет (новые)
            #         try:
            #             # img =
            #             New.objects.create(source='lenta.ru',
            #                                url=record[1],
            #                                date=timezone.now(),
            #                                category=record[0],
            #                                header=record[2],
            #                                text=record[3],
            #                                img=record[4])
            #                                # img1=record[5])
            #             print 'saved!!'
            #             qty_of_new += 1
            #         except:  # исключение падения базы из-за какой нить херни
            #             print 'database was crushed while saving new data'

            print 'updated', qty_of_new, 'news'
            print 'already have', miss, 'news'
            return HttpResponseRedirect('/')


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        slug = self.kwargs['article']
        for article in New.objects.all():
            if slug in article.url:
                context['article'] = article
        return context


class AllNewsView(TemplateView):
    template_name = 'allnews.html'

    def get_context_data(self, **kwargs):
        context = super(AllNewsView, self).get_context_data(**kwargs)
        curr_year = self.kwargs.values()[0]
        curr_day = self.kwargs.values()[1]
        curr_month = self.kwargs.values()[2]
        today = curr_year + '-' + curr_month + '-' + curr_day
        count = 0
        articles = []
        for article in New.objects.all().order_by('-id'):
            if unicode(article.date) >= today:
                count += 1
                articles.append(article)

        context['articles'] = articles
        context['count'] = count

        return context