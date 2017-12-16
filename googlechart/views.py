# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,  HttpResponse
import json

from django.shortcuts import redirect
# Create your views here.


def success_message(res_data, cookie_info = None):
    res = {}
    res['message'] = 'success'
    res['data'] = res_data
    response = HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
    if cookie_info is not None:
        for key in cookie_info:
            response.set_cookie(key, cookie_info[key], 3600)
    return response


def show_chart(request):
    return render(
        request,
        'show_chart.html'
    )

def update_data(request):
    data_path = '/home/give/PycharmProjects/MedicalImage/tools/loss_value'
    name = 'loss'
    train_data = []
    val_data = []
    with open(data_path) as filed:
        lines = filed.readlines()
        for line in lines[1:90]:
            array = line.split(' ')
            if name.startswith('loss'):
                train_data.append(float(array[1]))
                val_data.append(float(array[2]))
            elif name == 'accuracy':
                train_data.append(float(array[3]))
                val_data.append(float(array[4]))
    result_data = {}
    result_data['train_data'] = train_data
    result_data['val_data'] = val_data
    result_data['train_name'] = 'train ' + name
    result_data['val_name'] = 'val ' + name
    return success_message(result_data)