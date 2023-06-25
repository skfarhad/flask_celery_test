import sys
import os
from flask import Flask
from celery.result import AsyncResult
from ..worker.tasks import execute_add_async, app as celery_app

app = Flask(__name__)

@app.get("/result/<task_id>")
def task_result(task_id: str) -> dict[str, object]:
    result = AsyncResult(task_id, app=celery_app)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }

@app.route('/task/add')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    result = execute_add_async.delay(2, 3)
    RES_ID = result.id
    return {"result_id": result.id}


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='localhost', port=5000, debug=True)

