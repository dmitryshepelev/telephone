import datetime

from celery.task import periodic_task


@periodic_task(run_every=datetime.timedelta(seconds=10))
def cleanup_temp():
	print('hell')
	# open('%s.txt' % datetime.datetime.now().second, 'rw')