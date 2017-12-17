# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,  HttpResponse
from django.http import StreamingHttpResponse
import json
import numpy as np
import os

from django.shortcuts import redirect
# Create your views here.


def success_message(res_data, cookie_info = None):
    print 'return successful message'
    res = {}
    res['message'] = 'success'
    res['data'] = res_data
    response = HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
    if cookie_info is not None:
        for key in cookie_info:
            response.set_cookie(key, cookie_info[key], 3600)
    return response


def error_message(return_message={'message':'error'}):
    print 'return error message'
    return HttpResponse(json.dumps(return_message, ensure_ascii=False), content_type='application/json')


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


def show_attributes(request):
    if request.method == 'POST':
        print 'receive show_attributes function'
        max_count = int(1e6)
        if len(request.FILES.keys()) > 1:
            return error_message({
                'message': '目前只支持单个文件'
            })
        for key in request.FILES.keys():
            print key
            will_save_file = request.FILES.get(key)
            random_index = np.random.randint(1, max_count)
            saved_path = will_save_file.name + '_' + str(random_index) + '.txt'
            file_save_path = os.path.join(os.getcwd(), 'upload', saved_path)
            destination = open(file_save_path, 'wb+')
            for chunk in will_save_file.chunks():
                destination.write(chunk)
            destination.close()
            with open(file_save_path, 'rb+') as destination:
                line = unicode(destination.readline(), 'utf8')
                line = line.replace('\n', '')
                attributes = line.split(',')[1:]
                return success_message({'attributes': attributes, 'saved_name': os.path.join('upload', saved_path)})
        return success_message({})


def get_show_data(request):
    if request.method == 'POST':
        if len(request.FILES.keys()) > 1:
            return error_message({
                'message': '目前只支持单个文件'
            })
        saved_name = request.POST['saved_name']
        print request.POST
        if saved_name == '':
            # 没有执行show attributes的条件下，显示所有属性
            print 'the function do not finished'
        else:
            file_save_path = os.path.join(os.getcwd(), saved_name)
            attributes = []
            attribute_indexs = []
            for key in request.POST.keys():
                if key.startswith('attribute:') and request.POST[key] == 'true':
                    attributes.append(key[10:])
            with open(file_save_path, 'rb') as destination:
                lines = [unicode(line, 'utf8') for line in destination.readlines()]
                head_line = lines[0]
                head_line = head_line.replace('\n', '')
                attributes_all = head_line.split(',')
                for attribute_index, attribute in enumerate(attributes):
                    attribute_indexs.append(attributes_all.index(attribute))
                axis = []
                show_data = []
                for line in lines[1:]:
                    line = line.replace('\n', '')
                    array = line.split(' ')
                    axis.append(array[0])
                    item = [int(array[0])]
                    for item_index in attribute_indexs:
                        item.append(float(array[item_index]))
                    show_data.append(item)
                return success_message({
                    'axis': axis,
                    'show_data': show_data,
                    'attributes': attributes
                })
    else:
        return error_message({'message': 'should use the post method'})


def file_download(request):
    # do something...

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = os.path.join(os.getcwd(), 'loss_value')
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response