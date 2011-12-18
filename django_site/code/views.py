# -*- coding:utf-8 -*-

#native

#third-part
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django import forms
from douban.service import DoubanService
from douban.client import OAuthClient
#loacl
from private import API_KEY, API_SECRET, HOST

def plans(request):
    plans = db.get_all_config_data()
    return render_to_response('plans.htm', {'plans': plans})

def plan_detail(request, plan):
    #check.
    if not plan:
        raise Http404()
    #init.
    para = {}
    #display the steps list.
    plans = db.get_all_config_data()
    for item in plans:
        if item['PlanName'] == plan:
            para['plan'] = item
    #deal with add_step.
    if request.method == 'POST':
        if 'type' in request.POST:
            type = request.POST['type']
            para['add_step_detail_form'] = AddStepDetailForm(type)
    else:
        para['add_step_form'] = AddStepForm()

    return render_to_response('plan_detail.htm', para)

def home(request):
    render_para = {}
    #if no session found, a new user.
    if not request.session.get('access_token_key', False):
        client = OAuthClient(key=API_KEY, secret=API_SECRET)
        key, secret = client.get_request_token()
        auth_url = client.get_authorization_url(key, secret, callback = HOST)
        render_para['auth_url'] = auth_url
        return render_to_response('newcoming.htm',  render_para)
   
    #else session found

    return HttpResponse('hi')

