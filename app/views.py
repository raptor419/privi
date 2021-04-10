# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import QuestionSerializer
from .summarizer import *
from .question_generator import *


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")


def pages(request):
    context = {}
    # noinspection PyBroadException
    try:
        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:
        template = loader.get_template('pages/error-404.html')
        return HttpResponse(template.render(context, request))


def get_question_obj():
    try:
        snippet_received = get_snippet()
        questions_obj_list = make_questions(snippet_received)
        print(snippet_received.title)
    except ValueError:
        print("Error")
        return get_question_obj()
    return questions_obj_list,snippet_received


@csrf_exempt
def make_quiz(request):
    if request.method == 'GET':

        questions_obj_list, snippet_received = get_question_obj()
        # snippet_received = get_snippet()
        # questions_obj_list = make_questions(snippet_received)

        quiz_dict = {'success': True, 'statusCode': 201}

        data_dict = {'title': snippet_received.title}
        questions_dict = {}
        questions_parsed_list = []

        for x in questions_obj_list:
            questions_parsed_list.append(parse_question(x))

        questions_dict['questions'] = questions_parsed_list
        data_dict['quiz'] = questions_dict
        quiz_dict['data'] = data_dict
        return JsonResponse(quiz_dict, status=201)
