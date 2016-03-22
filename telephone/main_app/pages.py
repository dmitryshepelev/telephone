from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def st_page(request):
	return render_to_response('st_page.html', {}, context_instance=RequestContext(request))