from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
import json
import ast
from .form_basic import BasicForm, DetailForm
from .query import get_offers, get_details
from itertools import chain
import time

short_list = []
back = "shortlist"

# Create your views here.
def get_params(request):
    global data_dict
    global results
    global results_detail
    global info
    start = time.time()
    if request.method=="POST" and "find" in request.POST:
        form = BasicForm(request.POST)
        if form.is_valid():
            data_dict = request.POST
            results = get_offers(form.data)
    elif request.method=="POST" and "back" in request.POST:
        form = BasicForm(data_dict)
        results_detail = 1
        info = 0
    else:
        if 'results' in globals() and type(results) == list:
            form = BasicForm(data_dict)
        else:
            form = BasicForm()
            results = 3
    template = 'view1.html'
    page_template = 'endless.html'
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': #if request.is_ajax():
        template = 'endless.html'
    print(time.time() - start)
    return render(request, template, {'form': form, 'results': results, 'page_template': page_template})

def second_view(request):
    global data_dict
    global hotel_select
    global results_detail
    global data_dict_detail
    global info
    global short_list
    start = time.time()
    form = BasicForm(data_dict)
    data_dict = data_dict
    if request.method == "POST" and len(list(request.POST.keys())) == 2 and "short" in request.POST:
        el = [ast.literal_eval(request.POST["short"].split(";;")[0]), ast.literal_eval(request.POST["short"].split(";;")[1])]
        el = list(chain.from_iterable(el))
        if el in short_list:
            pass
        else:
            short_list.append(el)
    if request.method == "POST" and len(list(request.POST.keys()))==2 and "short" not in request.POST and "back" not in request.POST:
        hotel_select = int(list(request.POST.keys())[-1])
    if request.method == "POST" and "detail" in request.POST:
        detail_form = DetailForm(request.POST)
        if detail_form.is_valid():
            data_dict_detail = request.POST
            results_detail, info = get_details(form.data, hotel_select, detail_form.data)
    else:
        if 'results_detail' in globals() and type(results_detail) == list:
            detail_form = DetailForm(data_dict_detail)
        else:
            detail_form = DetailForm()
            results_detail = 1
            info = 0
    template = 'view2.html'
    page_template = 'endless_detail.html'
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': #if request.is_ajax():
        template = 'endless_detail.html'
    print(time.time() - start)
    return render(request, template, {'form': form, 'detail_form': detail_form, 'results': results_detail, 'info': info, 'page_template': page_template})


def short_list_view(request):
    global short_list
    global back
    if request.method == "POST" and "save-h" in request.POST:
        back = "home"
    if request.method == "POST" and "save-m" in request.POST:
        back = "more"
    if request.method == "POST" and "remove" in request.POST:
        el_remove = ast.literal_eval(request.POST["remove"])
        if el_remove in short_list:
            short_list.remove(el_remove)
            if short_list is None:
                short_list = []
    if len(short_list) == 0:
        short = 0
    else:
        short = list(reversed(short_list))
    template = 'shortlist_view.html'
    page_template = 'endless_shortlist.html'
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': #if request.is_ajax():
        template = 'endless_shortlist.html'
    return render(request, template, {'shortlist': short, 'back': back, 'page_template': page_template})