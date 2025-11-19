from flask import Flask, request
import time
from prometheus_client import Counter, Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


app = Flask(__name__)
REQS = Counter('requests_total', 'Total requests')
QUEUE = Gauge('fake_queue_length','simulated queue length')

@app.route('/')
def hello():
    REQS.inc()
    return "ok"

@app.route('/work')
def work():
    REQS.inc()
    t = int(request.args.get('t', '3'))
    end = time.time() + t
    # busy loop for CPU
    while time.time() < end:
        pass
    return f"done {t}s"

@app.route('/queue/<int:n>', methods=['POST'])
def set_queue(n):
    QUEUE.set(n)
    return "queue set"

# mount prometheus at /metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
