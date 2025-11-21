import time
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'django_request_count', 'Total HTTP requests', ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'django_request_latency_seconds', 'HTTP request latency in seconds', ['endpoint']
)

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        latency = time.time() - start_time

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            http_status=response.status_code
        ).inc()

        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
        return response