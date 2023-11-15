#!/usr/bin/env python3
import connexion

from swagger_server import encoder
from prometheus_flask_exporter import PrometheusMetrics
#from swagger_server.controllers.car_controller import metrics

app = connexion.App(__name__, specification_dir='./swagger/')

metrics = PrometheusMetrics(app.app)
#metrics.info("app_info", "Application Information", version="1.0.0")

def get_metrics():
    return metrics

def main():
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Автосалон'}, pythonic_params=True)
    app.run(port=8080)

if __name__ == '__main__':
    main()
