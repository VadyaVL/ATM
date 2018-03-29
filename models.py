#-*- coding:utf8 -*-
from django.db import models

# Описиваем нашу БД. Две таблицы:
# Банковские карты и операции.

class BankCard(models.Model):
    Number = models.TextField(primary_key=True, null=False, verbose_name="Номер")
    Password = models.TextField(null=False, verbose_name="Пароль")
    FailCount = models.IntegerField(null=False, verbose_name="Ошыбок ввода пароля", default=0)
    Balance = models.FloatField(null=False, verbose_name="Баланс")
    Locked = models.BooleanField(null=False, verbose_name="Заблокированая", default=False)

    class Meta:
        db_table = 'BankCard'

class Operation(models.Model):
    DateT = models.DateTimeField(null=False, verbose_name="Дата и время")
    Message = models.TextField(null=False, verbose_name="Сообщение")
    Card_Number = models.ForeignKey(BankCard)                               # Внешний ключ на банковские карты.

    class Meta:
        db_table = 'Operation'