from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from . import models
from django.db.models import Q
import os
import json
import datetime
from .xietong import UserCf


# Create your views here.


@login_required
def index(request):
    leixings = models.Case_item.objects.all()
    leixins = []
    for lei in leixings:
        if '笔记本' in lei.leixing:
            leixins.append(lei.leixing)
    leixins = list(set(leixins))[:5]
    if request.method == 'GET':
        datas1 = models.XinWei.objects.all()
        dicts = {}
        for data in datas1:
            if dicts.get(data.user.username, '') == '':
                dicts[data.user.username] = {}
                dicts[data.user.username][data.case_item.id] = data.nums
            else:
                dicts[data.user.username][data.case_item.id] = data.nums

        userCf = UserCf(data=dicts)
        r = userCf.recommend(request.user.username)
        if not r:
            datas = models.Case_item.objects.all()[:10]
        else:
            datas = []
            for rs in r:
                datas.append(get_object_or_404(models.Case_item, pk=rs[0]))

        xingping = models.Case_item.objects.all().order_by('-id')[:10]

        endtime = datetime.datetime.now()
        start_time = endtime + datetime.timedelta(hours=-1)

        renmings = models.Dianji.objects.filter(date__range=[start_time, endtime])
        dicts = {}
        for renm in renmings:
            if dicts.get(renm.case_item.id, '') == '':
                dicts[renm.case_item.id] = 1
            else:
                dicts[renm.case_item.id] = dicts[renm.case_item.id] + 1
        print(dicts)
        sorted(dicts.items(), key=lambda item: item[1], reverse=True)
        renming = []
        for ii in list(dicts.keys())[:10]:
            renming.append(get_object_or_404(models.Case_item, pk=ii))

        return render(request, 'apps/index.html', locals())


@login_required
def show_case(request):
    leixings = models.Case_item.objects.all()
    leixins = []
    for lei in leixings:
        if '笔记本' in lei.leixing:
            leixins.append(lei.leixing)
    leixins = list(set(leixins))[:5]
    if request.method == 'GET':
        itype = request.GET.get('itype')
        datas = models.Case_item.objects.filter(leixing__icontains=itype)
        nums = len(datas)
        return render(request, 'apps/shop.html', locals())


@login_required
def query_case(request):
    leixings = models.Case_item.objects.all()
    leixins = []
    for lei in leixings:
        if '笔记本' in lei.leixing:
            leixins.append(lei.leixing)
    leixins = list(set(leixins))[:5]
    if request.method == 'POST':
        data = request.POST
        name = data.get('sousuo')
        datas = models.Case_item.objects.filter(name__icontains=name).all()
        return render(request, 'apps/shop.html', locals())


def show_case_item(request, id):
    leixings = models.Case_item.objects.all()
    leixins = []
    for lei in leixings:
        if '笔记本' in lei.leixing:
            leixins.append(lei.leixing)
    leixins = list(set(leixins))[:5]
    if request.method == 'GET':
        datas = models.Case_item.objects.get(pk=id)
        if models.XinWei.objects.filter(Q(user=request.user) & Q(case_item=datas)):
            data = models.XinWei.objects.filter(Q(user=request.user) & Q(case_item=datas))[0]
            data.nums = data.nums + 1
            data.save()
        else:
            models.XinWei.objects.create(
                user=request.user,
                case_item=datas,
                nums=1
            )
        models.Dianji.objects.create(
            user=request.user,
            case_item=datas,
        )

        tuijian = models.Case_item.objects.filter(leixing=datas.leixing)
        if tuijian:
            tuijian = tuijian.order_by('-id')[:5]
        else:
            tuijian = models.Case_item.objects.all().order_by('-id')[:5]
        return render(request, 'apps/shop_item.html', locals())


@login_required
def dafen(request, id):
    leixings = models.Case_item.objects.all()
    leixins = []
    for lei in leixings:
        if '笔记本' in lei.leixing:
            leixins.append(lei.leixing)
    if request.method == 'GET':
        case = get_object_or_404(models.Case_item, pk=id)
        datas = models.DaFen.objects.filter(Q(user=request.user) & Q(case_item=case))
        if datas:
            fenshu = datas[0].fenshu
        else:
            fenshu = ''
        return render(request, 'apps/dafen.html', locals())

    elif request.method == 'POST':
        case = get_object_or_404(models.Case_item, pk=id)
        data = request.POST
        fenshu = data.get('fenshu')
        if not models.DaFen.objects.filter(Q(user=request.user) & Q(case_item=case)):
            models.DaFen.objects.create(
                user=request.user,
                case_item=case,
                fenshu=fenshu
            )
        else:
            models.DaFen.objects.filter(Q(user=request.user) & Q(case_item=case)).update(
                fenshu=fenshu
            )

        return redirect('shop:show_case_item', id)
