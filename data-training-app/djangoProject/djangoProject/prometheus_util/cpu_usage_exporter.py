import logging
import os

from prometheus_client import Gauge
import psutil

from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

system_cpu_usage = Gauge('system_cpu_usage', 'System CPU usage')
memory_usage = Gauge('memory_usage', 'Memory usage')

logger = logging.getLogger(__name__)


def update_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    system_cpu_usage.set(cpu_usage)


def get_memory_usage():
    memory_usage.set(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

def metrics(request):
    metrics_data = generate_latest()
    update_cpu_usage()
    get_memory_usage()
    return HttpResponse(metrics_data, content_type=CONTENT_TYPE_LATEST)
