#-*- coding:cp1251 -*-
# ��� ����������� ������ �� �������
from django.shortcuts import render, redirect
import models       # ����������� ������ ��� ������ � ����
import datetime     # ��� ��������� ��������� �������
"""
 �������� ������ � ������, ������� ��� � ������
"""
""" �������������� ����������: ������� �� �������� �����, ����� ���� �����,
    ������ �� ��������� ������ � ���������� ������.
    ��� ����� ������� � ������� HTTP-cookie, �� � ����� ���� ������ ���������� �� � �������(� ��������),
    � ������ �� �������."""
card = False
num = 0
passw = False
pas = 0

# ����� ��� ��������� ������� ��������
def home(request):
    global card, num, passw, pas    # ������� ��� ���������� ���������� ����������

    if card and passw:              # ���� �� �����, �� ���������������� �� ��������� � ����������
        return redirect('/operation/')
    elif not card:                  # ���� ��� �� ����� ��������
        if request.POST:            # ��������� ������ �� ����� POST � ������� �����
            number = request.POST['number'].replace('-', '')        # ����� ����� ����� � POST ������ �����������
            object = models.BankCard.objects.filter(Number=number)  # �������� �� ������� ������ - ���������� �����
            if len(object) == 0:        # ���� ���� �����
                arg = {}                # ��������� ������ ����-��������
                arg['type'] = 1         # �������
                arg['Title'] = 'Error'  # ��� ��� ������ � ������� ��
                arg['mess'] = 'Asking the bank card is not in the database.'   # ������ ��������� ������
                return render(request, 'mess.html', arg)    # ���������� ������
            elif object[0].Locked:                          # ���� �������� ���� � ��� �������������
                arg = {}                                    # ��������� ������ ����-��������
                arg['type'] = 1                             # �������
                arg['Title'] = 'Error'                      # ��� ��� ������ � ������� ��
                arg['mess'] = 'Asking a bank card is locked.'        # ������ ��������� ������
                return render(request, 'mess.html', arg)    # ���������� ������
            else:                                           # � ���� ������ ��� ������ - ����� ����
                card = True                                 # ������� ��� ����� �������. ����� � ���� ���������.
                num = request.POST['number']                # ��������� ����� ����� ��� ����������� �����������. ����� � ����.
    else:                                   # ��� �� ����� ������ �� ����� ��������
        if request.POST:                    # ��������� ������ �� ����� POST � ������� �����
            if 'exit' in request.POST:      # ���� ����� ����� � POST
                card=False                  # �������, ��������� ���������� � �������� ��������
            else:                           # ���� �� �����
                pas = request.POST['passw'] # �������� ������ � POST
                object = models.BankCard.objects.filter(Number=num.replace('-', ''))[0]    # ���� �����
                if object.Password == pas:          # ���� ������ ��������
                    passw = True                    # ������� ��� ������ ������
                    return redirect('/operation/')  # ��������� � ���������
                else:                               # ���� ������ �� ��������
                    arg = {}                        # ��������� ������ ����-��������
                    arg['type'] = 1                 # �������
                    arg['Title'] = 'Error'          # ��� ��� ������ � ������� ��
                    object.FailCount = object.FailCount + 1     # ����������� ������� �������� ������� ����� ������
                    # ������ ��������� ������ � ������� ������� �������� �������
                    arg['mess'] = 'Incorrect password! Attempts remaining ' + str(4-(object.FailCount)) + '.'

                    if object.FailCount == 4:       # ���� ������ ���� ����� �� �����
                        object.Locked = True        # ��������� �����
                        card = False                # ���������� �������� �����
                        arg['mess'] = arg['mess'] + ' Bank Card blocked!'  # + ������ � ��������� ����� �������������
                    object.save()
                    return render(request, 'mess.html', arg)            # ���������� ������

    return render(request, 'home.html', {'card': card, 'number': num})  # ���������� ������� ��������

# ���������� ����� �����
def add(request):
    if request.POST:
        number = request.POST['n']      # �������� �� POST ����� �����
        password = request.POST['p']    # �������� �� POST ������
        money = request.POST['m']       # �������� �� POST ���������� ����� �� ����� �����
        # ��������� ��� �� ����� ������� ������, ������� ����� � ��������� ��
        if number.isdigit() and len(number) == 16 and password.isdigit() and len(password) == 4 and money!='':
            obj = models.BankCard()
            obj.Number = number
            obj.Password = password
            obj.Balance = float(money)
            obj.save()
        else:         # ����� ������
            arg = {}
            arg['type'] = 1
            arg['Title'] = 'Error'
            arg['mess'] = 'One or more fields are filled with incorrect.'
            return render(request, 'mess.html', arg)

    return render(request, 'add.html')  # ���������� ������� ����������

# �������� ���� ���� � ��������
def viewAllCard(request):
    arg = {}                                        # ��������� ������ ����-��������
    arg['list'] = models.BankCard.objects.all()     # �������� ��� �����
    arg['oplist'] = models.Operation.objects.all()  # �������� ��� ��������
    return render(request, 'show.html', arg)        # ���������� ��� �������� � �����

def operation(request):
    global card, num, passw, pas    # ������� ��� ���������� ���������� ����������
    arg = {}                        # ��������� ������ ����-��������
    arg['index'] = 0                # index - �������� �� ��������, �� ���� ������, � ����������� �� ��� ��������
                                    # ���������� ������ ����������
    if not card and not passw:      # ���� ��� ����� � ��� ������ �� ���� �� �������� ��������
        return redirect('/home/')
    if 'exit' in request.POST:      # ���� ������ ������ �����
        card = False                # ����� ����� � ���� �� �������� ��������
        num = 0
        passw = False
        pas = 0
        return redirect('/home/')
    elif 'balance' in request.POST: # �������� �������
        arg['index'] = 1            # ������ ������ ��������
        arg['num'] = num            # ����� �����
        arg['datetime'] = datetime.datetime.now()   # ����� ��������
        # ������ �����
        arg['balance'] = models.BankCard.objects.filter(Number=num.replace('-', ''))[0].Balance
        op = models.Operation()     # ��������� ��������� �� �������� �������� �������
        op.Card_Number = models.BankCard.objects.filter(Number=num.replace('-', ''))[0]
        op.Message = 'View balance: ' + str(arg['balance'])
        op.DateT = arg['datetime']
        op.save()
    elif 'getMoney' in request.POST:# ������ �����
        arg['index'] = 2            # ������ ������ ��������
        arg['num'] = num            # ����� �����
    elif 'getMyMoney' in request.POST:      # ������� ������
        obj = models.BankCard.objects.filter(Number=num.replace('-', ''))[0]
        if obj.Balance > float(request.POST['money']):  # ���� ����� ����� ������������� �����
            obj.Balance = obj.Balance - float(request.POST['money'])
            obj.save()
            op = models.Operation()
            op.Card_Number = models.BankCard.objects.filter(Number=num.replace('-', ''))[0]
            op.Message = 'Get money: ' + request.POST['money']
            op.DateT = datetime.datetime.now()
            op.save()           # ������� �����
            # ���� ��������� �������� � �����������.
            arg['index'] = 3    # �������� ����������
            arg['num'] = num
            arg['datetime'] = datetime.datetime.now()
            arg['sum'] = float(request.POST['money'])
            arg['balance'] = obj.Balance
        else:   # ���� �� ����� ����� ������������� �����
            arg = {}
            arg['type'] = 1
            arg['Title'] = 'Error'
            arg['mess'] = 'The requested amount exceeds the card balance.'
            return render(request, 'mess.html', arg)
        pass

    return render(request, 'Operation.html', arg)
