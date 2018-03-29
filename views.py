#-*- coding:cp1251 -*-
# Для возможности писать на русском
from django.shortcuts import render, redirect
import models       # импортируем модели для работы с ними
import datetime     # для получения поточного времени
"""
 улучшить ошыбки и дизайн, собрать все и готово
"""
""" Дополнительные переменные: введена ли коректна карта, номер этой карты,
    введен ли коректный пароль и собственно пароль.
    Это лучше сделать с помощью HTTP-cookie, но в целях лабы храним информацию не у клиента(в браузере),
    а храним на сервере."""
card = False
num = 0
passw = False
pas = 0

# Метод для обработки главной страницы
def home(request):
    global card, num, passw, pas    # Говорим что используем глобальные переменные

    if card and passw:              # Если мы вошли, то перенаправляемся на страничку с операциями
        return redirect('/operation/')
    elif not card:                  # Если еще не ввели карточку
        if request.POST:            # Проверяем пришел ли метод POST с номером карты
            number = request.POST['number'].replace('-', '')        # Берем номер карты с POST удаляя разделитель
            object = models.BankCard.objects.filter(Number=number)  # Получаем по запросу обьект - банковскую карту
            if len(object) == 0:        # Если нету карты
                arg = {}                # Обьявляем список ключ-значение
                arg['type'] = 1         # Говорим
                arg['Title'] = 'Error'  # что это ошыбка и назывем ее
                arg['mess'] = 'Asking the bank card is not in the database.'   # Задаем сообщение ошыбки
                return render(request, 'mess.html', arg)    # Отображаем ошыбку
            elif object[0].Locked:                          # Если карточка есть и она заблокирована
                arg = {}                                    # Обьявляем список ключ-значение
                arg['type'] = 1                             # Говорим
                arg['Title'] = 'Error'                      # что это ошыбка и назывем ее
                arg['mess'] = 'Asking a bank card is locked.'        # Задаем сообщение ошыбки
                return render(request, 'mess.html', arg)    # Отображаем ошыбку
            else:                                           # В ином случае все хорошо - карта есть
                card = True                                 # Говорим что карта найдена. Можно в куки сохранить.
                num = request.POST['number']                # Сохраняем номер карты для дальнейшего отображения. Можно в куки.
    else:                                   # Еще не имеем пароль но имеем карточку
        if request.POST:                    # Проверяем пришел ли метод POST с номером карты
            if 'exit' in request.POST:      # Если имеем выход в POST
                card=False                  # Выходим, сбрасивая информацию о найденой карточке
            else:                           # Если не выход
                pas = request.POST['passw'] # Получаем пароль с POST
                object = models.BankCard.objects.filter(Number=num.replace('-', ''))[0]    # Ищем карту
                if object.Password == pas:          # Если пароль подходит
                    passw = True                    # Говорим что пароль верный
                    return redirect('/operation/')  # Переходим к операциям
                else:                               # Если пароль НЕ подходит
                    arg = {}                        # Обьявляем список ключ-значение
                    arg['type'] = 1                 # Говорим
                    arg['Title'] = 'Error'          # что это ошыбка и назывем ее
                    object.FailCount = object.FailCount + 1     # Увеличиваем счетчик неверных попыток ввода пароля
                    # Задаем сообщение ошыбки и говорим сколько осталось попыток
                    arg['mess'] = 'Incorrect password! Attempts remaining ' + str(4-(object.FailCount)) + '.'

                    if object.FailCount == 4:       # Если четыре раза ввели не верно
                        object.Locked = True        # Блокируем карту
                        card = False                # Сбрасываем найденую карту
                        arg['mess'] = arg['mess'] + ' Bank Card blocked!'  # + задаем в сообщение КАРТА ЗАБЛОКИРОВАНА
                    object.save()
                    return render(request, 'mess.html', arg)            # Отображаем ошыбку

    return render(request, 'home.html', {'card': card, 'number': num})  # Отображаем главную страницу

# Добавление новой карты
def add(request):
    if request.POST:
        number = request.POST['n']      # Получаем из POST номер карты
        password = request.POST['p']    # Получаем из POST пароль
        money = request.POST['m']       # Получаем из POST количество денег на новой карте
        # Проверяем все ли числа заданой длинны, создаем карту и сохраняем ее
        if number.isdigit() and len(number) == 16 and password.isdigit() and len(password) == 4 and money!='':
            obj = models.BankCard()
            obj.Number = number
            obj.Password = password
            obj.Balance = float(money)
            obj.save()
        else:         # Иначе ошыбка
            arg = {}
            arg['type'] = 1
            arg['Title'] = 'Error'
            arg['mess'] = 'One or more fields are filled with incorrect.'
            return render(request, 'mess.html', arg)

    return render(request, 'add.html')  # Отображаем главную добавления

# Просмотр всех карт и операций
def viewAllCard(request):
    arg = {}                                        # Обьявляем список ключ-значение
    arg['list'] = models.BankCard.objects.all()     # Получаем все карты
    arg['oplist'] = models.Operation.objects.all()  # Получаем все операции
    return render(request, 'show.html', arg)        # Отображаем все операции и карты

def operation(request):
    global card, num, passw, pas    # Говорим что используем глобальные переменные
    arg = {}                        # Обьявляем список ключ-значение
    arg['index'] = 0                # index - отвечает за операцию, по сути влажок, в зависимости от его значения
                                    # отображаем нужную информацию
    if not card and not passw:      # если нет карты и нет пароля то йдем на домашнюю страницу
        return redirect('/home/')
    if 'exit' in request.POST:      # Если нажата кнопка выход
        card = False                # сброс всего и йдем на домашнюю страницу
        num = 0
        passw = False
        pas = 0
        return redirect('/home/')
    elif 'balance' in request.POST: # Просмотр баланса
        arg['index'] = 1            # Ставим индекс операции
        arg['num'] = num            # Номер карты
        arg['datetime'] = datetime.datetime.now()   # Время операции
        # Баланс карты
        arg['balance'] = models.BankCard.objects.filter(Number=num.replace('-', ''))[0].Balance
        op = models.Operation()     # Сохраняем ведомости об операции просмотр баланса
        op.Card_Number = models.BankCard.objects.filter(Number=num.replace('-', ''))[0]
        op.Message = 'View balance: ' + str(arg['balance'])
        op.DateT = arg['datetime']
        op.save()
    elif 'getMoney' in request.POST:# Снятие денег
        arg['index'] = 2            # Ставим индекс операции
        arg['num'] = num            # Номер карты
    elif 'getMyMoney' in request.POST:      # Снимаем деньги
        obj = models.BankCard.objects.filter(Number=num.replace('-', ''))[0]
        if obj.Balance > float(request.POST['money']):  # Если можно снять запрашываемую сумму
            obj.Balance = obj.Balance - float(request.POST['money'])
            obj.save()
            op = models.Operation()
            op.Card_Number = models.BankCard.objects.filter(Number=num.replace('-', ''))[0]
            op.Message = 'Get money: ' + request.POST['money']
            op.DateT = datetime.datetime.now()
            op.save()           # успешно сняли
            # Надо загрузить страницу с результатом.
            arg['index'] = 3    # Просмотр результата
            arg['num'] = num
            arg['datetime'] = datetime.datetime.now()
            arg['sum'] = float(request.POST['money'])
            arg['balance'] = obj.Balance
        else:   # Если НЕ можно снять запрашываемую сумму
            arg = {}
            arg['type'] = 1
            arg['Title'] = 'Error'
            arg['mess'] = 'The requested amount exceeds the card balance.'
            return render(request, 'mess.html', arg)
        pass

    return render(request, 'Operation.html', arg)
