from django.shortcuts import render_to_response


def main(request, template):
	return render_to_response(template, {})
