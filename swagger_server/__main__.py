#!/usr/bin/env python3
import connexion

from swagger_server import encoder
from prometheus_flask_exporter import PrometheusMetrics

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
  TracerProvider(
    resource=Resource.create({SERVICE_NAME: "Showroom"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="jaeger",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

app = connexion.App(__name__, specification_dir='./swagger/')

metrics = PrometheusMetrics(app.app)

def get_metrics():
    return metrics

def main():
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Автосалон'}, pythonic_params=True)
    app.run(port=8080)

if __name__ == '__main__':
    main()
