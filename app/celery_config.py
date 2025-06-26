from celery import Celery

def make_celery():
    celery_app = Celery("flask-queue")
    celery_app.conf.update(
        broker="amqp://guest:guest@localhost//",
        result_backend="rpc://",
    )
    return celery_app
