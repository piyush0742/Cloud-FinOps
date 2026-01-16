from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

def setup_telemetry(service_name: str):
    trace.set_tracer_provider(TracerProvider())
    tracer_provider = trace.get_tracer_provider()
    exporter = OTLPSpanExporter()
    tracer_provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )
