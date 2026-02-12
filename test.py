import random
import time
import opentelemetry

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry import metrics
from opentelemetry.metrics import Observation

# ---- OTel Setup ----

exporter = OTLPMetricExporter(
    endpoint="http://otelcol:4318/v1/metrics",  #OTEL collector
)

reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=2000  # export every 2 seconds
)

provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("dummy-metrics-generator")

# ---- Metric Instruments ----

cpu_metric = meter.create_gauge(
    name="cpu_usage",
    description="Dummy CPU usage percentage",
    unit="percent"
)

memory_metric = meter.create_gauge(
    name="memory_usage",
    description="Dummy memory usage percentage",
    unit="percent"
)

disk_metric = meter.create_gauge(
    name="disk_usage",
    description="Dummy disk usage percentage",
    unit="percent"
)

# ---- Dummy Metric Generator ----

def generate_dummy_metrics():
    return {
        "cpu": round(random.uniform(0, 100), 2),
        "memory": round(random.uniform(0, 100), 2),
        "disk": round(random.uniform(0, 100), 2),
    }

# ---- Main Loop ----

if __name__ == "__main__":
    print("Starting OTel dummy metric generator...")

    while True:
        data = generate_dummy_metrics()

        cpu_metric.set(data["cpu"])
        memory_metric.set(data["memory"])
        disk_metric.set(data["disk"])

        print(f"CPU: {data['cpu']}% | Memory: {data['memory']}% | Disk: {data['disk']}%")

        time.sleep(2)