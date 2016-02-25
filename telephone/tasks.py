from telephone.celery import app


@app.task(name='add_task')
def add(x, y):
	return x + y