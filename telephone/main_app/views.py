from django.shortcuts import render_to_response
from django.template import RequestContext


def main(request, template):
	return render_to_response(template, {}, context_instance=RequestContext(request))
