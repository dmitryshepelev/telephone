from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.settings import BASE_DIR


def main(request, template):
	return render_to_response(template, {}, context_instance=RequestContext(request))


@login_required
def stat(request, template):
	return render_to_response(template, {}, context_instance=RequestContext(request))


@login_required()
def get_test_file(request):
	abspath = open(BASE_DIR + '/static/content/test.csv', 'r')
	response = HttpResponse(content=abspath.read())
	response['Content-Type'] = 'text'
	return response