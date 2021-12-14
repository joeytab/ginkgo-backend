from django.shortcuts import render
from .models import Response
from .serializers import ResponseSerializer
from rest_framework import viewsets
from django.http import HttpResponse
from django.views.generic import View
import json
import os
import sys
import time

from rq import Queue

sys.path.append(os.path.dirname(__file__))
from align import searchSeq
from worker import conn

q = Queue(connection=conn)
# Create your views here.

class ResponseView(viewsets.ViewSet):
    serializer_class = ResponseSerializer
    queryset = Response.objects.values() #.values['sequence']
    # def list(self, request):
    #     data = {"nt_searches": "testing"}
    #     return HttpResponse(data, content_type="application/json")
    # self.allowed_methods = ['get', 'post', 'options']
    def options(self, request, id):
        print("get options")
        response = HttpResponse()
        # response['allow'] = ','.join([self.allowed_methods])
        response.headers['Access-Control-Allow-Headers'] = 'origin, content-type, accept'
        response.headers['Access-Control-Allow-Origin'] = 'https://ginkgo-frontend.herokuapp.com/'
        response.headers['Access-Control-Allow-Methods'] = "GET,POST,OPTIONS"
        print(response.headers)
        return response
    def create(self, request):
        sequence = request.POST.get('sequence')
        self.queryset = Response.objects.values()
        job = q.enqueue(searchSeq, args = (sequence,), job_timeout = 600)
        HttpResponse("Waiting...")
        while(job.result == None):
            print("waiting...")
            time.sleep(10)
        responses = job.result
        # responses = searchSeq(self.queryset[0]['sequence'])
        print("got job result")
        data = json.dumps(responses)
        print("data " + data)
        return HttpResponse(data, content_type="application/json")
        # http.headers['Access-Control-Allow-Headers'] = 'origin, content-type, accept'
        # http.headers['Access-Control-Allow-Origin'] = '*'
        # http.headers['Access-Control-Allow-Methods'] = "GET,POST,OPTIONS"
        # return http
    def django_models_json(request):
        responses = list(queryset)
        data = json.dumps(responses)
        return HttpResponse(data, content_type="application/json",
        headers = {'Access-Control-Allow-Origin': 'https://ginkgo-frontend.herokuapp.com/'})
