# -*- coding:utf-8 -*-

import datetime
import os
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from summary import utils
from summary import models
from summary.sheets.profitsheet import ProfitSheet
from summary.sheets.costsheet import CostSheet
from summary.sheets.salessheet import SalesSheet
from summary.sheets.managementcostsheet import ManagementCostSheet
from summary.sheets.financialexpensessheet import FinancialExpensesSheet
from summary.sheets.taxespayablesheet import TaxesPayableSheet
from summary.sheets.taxespaidsheet import TaxesPaidSheet
from summary.sheets.laborcostsheet import LaborCostSheet
from summary.sheets.depreciationsheet import DepreciationSheet

def login(request) :
    context = RequestContext(request)
    context['login_error'] = False
    if request.method == 'POST' :
        user_name = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(username = user_name, password = password)
        if user is not None :
            _login(request, user)
            return redirect(reverse('summary:index'))
        else :
            try :
                user = User.objects.get(username = user_name)
            except User.DoesNotExist, e :
                register_url = reverse('summary:register')
                return redirect('%s?user_name=%s'  %(register_url, user_name))
            context['login_error'] = True
    return render(request, 'summary/login.html', context)


def register(request) :
    context = RequestContext(request)
    context['register_error'] = 0
    context['user_name'] = ''
    if request.method == 'POST' :
        user_name = request.POST['user_name']
        password = request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST['email']
        try :
            user = User.objects.get(username = user_name)
        except User.DoesNotExist, e :
            user = None
        if len(user_name) == 0 :
            context['register_error'] = -1
            return render(request, 'summary/register.html', context)
        if len(password) == 0 :
            context['register_error'] = -2
            return render(request, 'summary/register.html', context)
        if len(email) == 0 :
            context['register_error'] = -3
            return render(request, 'summary/register.html', context)
        if user is not None :
            context['register_error'] = -4
            return render(request, 'summary/register.html', context)
        if (password) != repassword :
            context['register_error'] = -5
            return render(request, 'summary/register.html', context)
        user = User.objects.create_user(user_name, email, password)
        user.save()
        context['register_error'] = 1
    else :
        context['user_name'] = request.GET.get('user_name', '')
    return render(request, 'summary/register.html', context)


@login_required(login_url = '/summary/login/')
def logout(request) :
    _logout(request)
    return redirect(reverse('summary:login'))


@login_required(login_url = '/summary/login/')
def index(request) :
    context = RequestContext(request)
    return render(request, 'summary/index.html', context)


@login_required(login_url = '/summary/login/')
def workbook(request) :
    context = RequestContext(request)
    context['parsetasks'] = models.ParseTask.objects.filter(author = request.user.username)
    thisyear = datetime.date.today().year
    context['years'] = range(thisyear, thisyear-5, -1)
    return render(request, 'summary/workbook.html', context)


@login_required(login_url = '/summary/login/')
def workbook_upload(request) :
    if request.method == 'POST' :
        workbook_year = request.POST['workbook_year']
        workbook_name = request.POST['workbook_name']
        workbook_file = request.FILES['workbook_file']
        today = datetime.date.today()
        workbook_dir = os.path.join(settings.MEDIA_ROOT,\
                request.user.username,\
                str(today.year),\
                str(today.month),\
                str(today.day))
        if not os.path.isdir(workbook_dir) :
            os.makedirs(workbook_dir)
        workbook_hash = utils.md5_encode(workbook_name.encode('utf-8'))
        workbook_path = os.path.join(workbook_dir, workbook_hash)
        if os.path.isfile(workbook_path) :
            os.remove(workbook_path)
        with open(workbook_path, 'wb+') as workbook_fp :
            for chunk in workbook_file :
                workbook_fp.write(chunk)
            workbook_fp.close()
        hashid = utils.md5_encode(workbook_path)
        try :
            models.ParseTask.objects.get(hashid = hashid)
        except models.ParseTask.DoesNotExist :
            task = models.ParseTask()
            task.hashid = hashid
            task.author = request.user.username
            task.year = workbook_year
            task.filename = workbook_name
            task.parsefile = workbook_path
            task.save()
    return redirect(reverse('summary:workbook'))

@login_required(login_url = '/summary/login/')
def sheet(request, hashid) :
    context = RequestContext(request)
    context['hashid'] = hashid
    context['sheets'] = [
        {
            'id' : 'profit',
            'tabs' : ProfitSheet.name,
            'selected' : True,
        },
        {
            'id' : 'cost',
            'tabs' : CostSheet.name,
            'selected' : False,
        },
        {
            'id' : 'sales',
            'tabs' : SalesSheet.name,
            'selected' : False,
        },
        {
            'id' : 'managementcost',
            'tabs' : ManagementCostSheet.name,
            'selected' : False,
        },
        {
            'id' : 'financialexpenses',
            'tabs' : FinancialExpensesSheet.name,
            'selected' : False,
        },
        {
            'id' : 'taxespayable',
            'tabs' : TaxesPayableSheet.name,
            'selected' : False,
        },
        {
            'id' : 'taxespaid',
            'tabs' : TaxesPaidSheet.name,
            'selected' : False,
        },
        {
            'id' : 'laborcost',
            'tabs' : LaborCostSheet.name,
            'selected' : False,
        },
        {
            'id' : 'depreciation',
            'tabs' : DepreciationSheet.name,
            'selected' : False,
        },
    ]
    return render(request, 'summary/sheet.html', context)


@login_required(login_url = '/summary/login/')
def table(request, hashid, table) :
    context = RequestContext(request)
    context['hashid'] = hashid
    context['tableid'] = table
    if 'profit' == table :
        context['data'] = ProfitSheet.format(hashid)
    elif 'cost' == table :
        context['data'] = CostSheet.format(hashid)
    elif 'sales' == table :
        context['data'] = SalesSheet.format(hashid)
    elif 'managementcost' == table :
        context['data'] = ManagementCostSheet.format(hashid)
    elif 'financialexpenses' == table :
        context['data'] = FinancialExpensesSheet.format(hashid)
    elif 'taxespayable' == table :
        context['data'] = TaxesPayableSheet.format(hashid)
    elif 'taxespaid' == table :
        context['data'] = TaxesPaidSheet.format(hashid)
    elif 'laborcost' == table :
        context['data'] = LaborCostSheet.format(hashid)
    elif 'depreciation' == table :
        context['data'] = DepreciationSheet.format(hashid)
    return render(request, 'summary/'+table+'.html/', context)

