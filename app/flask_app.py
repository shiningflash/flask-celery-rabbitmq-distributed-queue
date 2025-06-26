from flask import Flask, request
from celery.result import AsyncResult
from app.tasks import async_send_email, async_parse_exploits, celery_app

def create_app():
    app = Flask(__name__)
    register_routes(app)
    return app


def register_routes(app):

    @app.route("/")
    def root():
        return "<h2>Flask + Celery + RabbitMQ</h2>"

    @app.route("/send_email", methods=["POST"])
    def send_email():
        data = request.json
        task = async_send_email.delay(data['email'], data['subject'], data['body'])
        return {"task_id": task.id}

    @app.route("/parse_exploits", methods=["POST"])
    def parse_exploits():
        task = async_parse_exploits.delay()
        return {"task_id": task.id}

    @app.route("/check_task/<task_id>")
    def check_task(task_id):
        result = AsyncResult(task_id, app=celery_app)
        return {
            "task_id": result.id,
            "status": result.status,
            "result": result.result
        }
