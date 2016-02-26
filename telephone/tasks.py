from telephone.celery import app


@app.task(name='add_task')
def add(x, y):
	return x + y


@app.task(name='send_mail')
def send_mail(mail_message):
	"""
	Task to send mail async
	:param mail_message:
	:return:
	"""
	result = mail_message.send()
	return result