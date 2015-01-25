#coding: utf8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Polls(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, verbose_name=u"Имя")
    time = models.DateTimeField(default=datetime.now(), null=True, verbose_name=u"Время")

    def __unicode__(self):
        return u"[#%s] %s" % (self.id, self.name)

    class Meta:
        verbose_name = u'Опрос'
        verbose_name_plural = u'Опросы'


class Options(models.Model):
    id = models.AutoField(primary_key=True)
    # Я хз зачем south попросил default значение, ну ок
    poll = models.ForeignKey(Polls, verbose_name=u"ID голосования")
    name = models.CharField(max_length=50, verbose_name=u"Имя")
    count = models.IntegerField(verbose_name=u"Счётчик", default=0)

    def __unicode__(self):
        return u"[#%s:%s] %s" % (self.poll_id, self.id, self.name)

    class Meta:
        verbose_name = u'Вариант'
        verbose_name_plural = u'Варианты'


class OptionsVotes(models.Model):
    id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(Polls, verbose_name="ID голосования")
    vote_id = models.IntegerField(verbose_name="ID варианта")
    user_ip = models.CharField(max_length=25, verbose_name="IP юзера")
    time = models.DateTimeField(default=datetime.now(), null=True, verbose_name="Время")


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(Polls, verbose_name="ID голосования")
    #name = models.CharField(max_length=15, verbose_name="Имя")
    user = models.ForeignKey(User, null=True)
    text = models.CharField(max_length=100, verbose_name="Текст")
    user_ip = models.CharField(max_length=25, verbose_name="IP юзера")
    time = models.DateTimeField(default=datetime.now(), null=True, verbose_name="Время")

    def __unicode__(self):
        return "[#%s] %s" % (self.poll_id, self.text)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'