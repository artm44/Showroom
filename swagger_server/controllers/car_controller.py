import connexion
import six
import time

from flask import request
from swagger_server.models.car import Car  # noqa: E501
from swagger_server import util
from flask import jsonify
from prometheus_flask_exporter import PrometheusMetrics
from swagger_server.models.repository import showroom
from swagger_server.__main__ import get_metrics

metrics = get_metrics()
metrics.info("app_info", "Application Information", version="1.0.0")

from opentelemetry import trace

tracer = trace.get_tracer(__name__)


import logging
import logging_loki


handler = logging_loki.LokiHandler(
    url="http://loki:3100/loki/api/v1/push", 
    tags={"application": "Showroom-app"},
    version="1",
)

logger = logging.getLogger("my-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

car_counter = metrics.counter(
    'cnt_car', 'Number of invocations per car', labels={
        'car': lambda: request.view_args['carId']
    })

@car_counter
@tracer.start_as_current_span(name="cars_car_id_delete")
def cars_car_id_delete(car_id):  # noqa: E501
    """cars_car_id_delete

    Получение информации о госте по номеру # noqa: E501

    :param car_id: 
    :type car_id: int

    :rtype: None
    """
    logger.info(f'Попытка удаления автомобиля', extra={'tags': {"car": car_id, "funcName": "cars_car_id_put"}})
    for car in showroom.Cars:
        if car._id == car_id:
            showroom.Cars.remove(car)
            logger.debug(f'Успешное удаление автомобиля', extra={'tags': {"car": car_id, "funcName": "cars_car_id_put", "status_code":200}})
            return '200'
    logger.warning(f'Неуспешная попытка удаления автомобиля', extra={'tags': {"car": car_id, "funcName": "cars_car_id_put", "status_code":400}})
    return '400'

@car_counter
@tracer.start_as_current_span(name="cars_car_id_get")
def cars_car_id_get(car_id):  # noqa: E501
    """cars_car_id_get

    Получение информации о госте по номеру # noqa: E501

    :param car_id: 
    :type car_id: int

    :rtype: Car
    """
    logger.info(f'Попытка получения автомобиля', extra={'tags': {"car": car_id, "funcName": "cars_car_id_get"}})
    for car in showroom.Cars:
        if car._id == car_id:
            return car.to_dict(), '200'
    logger.warning(f'Неуспешная попытка получения автомобиля', extra={'tags': {"car": car_id, "funcName": "cars_car_id_get", "status_code":400}})
    return '400'

@car_counter
@tracer.start_as_current_span(name="cars_car_id_put")
def cars_car_id_put(car_id, body=None):  # noqa: E501
    """Обновление автомобиля

    Изменение информации об автомобиле по номеру id # noqa: E501

    :param car_id: 
    :type car_id: int
    :param body: 
    :type body: dict | bytes

    :rtype: Car
    """
    logger.info(f'Попытка обновления автомобиля', extra={'tags': {"car": car_id, "funcName": "cars_car_id_put"}})
    if connexion.request.is_json:
        body = Car.from_dict(connexion.request.get_json())  # noqa: E501
    for i in range(len(showroom.Cars)):
        if (showroom.Cars[i]._id == car_id):
            body.id = car_id
            showroom.Cars[i] = body
            logger.debug(f'Успешное обновление автомобиля', extra={'tags': {"car": car_id, "funcName": "cars_car_id_put", "status_code":200}})
            return '200'
    return '400'

@metrics.summary('get_duration_seconds_sum', 'Get request latencies',
                 labels={'status': lambda r: r.status_code})
@metrics.gauge('get_in_progress', 'Long running requests in progress')
@tracer.start_as_current_span(name="cars_get")
def cars_get():  # noqa: E501
    """cars_get

    Получение списка автомобилей в автосалоне # noqa: E501

    :rtype: List[Car]
    """
    time.sleep(1)
    with tracer.start_as_current_span(name="sleep"):
        time.sleep(3)
    time.sleep(1)
    logger.info(f'Запрос списка автомобилей', extra={'tags': {"funcName": "cars_get", "status_code":200}})
    return jsonify(showroom.Cars), '200'

@metrics.counter('cnt_post', 'Number of invocations cars post', labels={
        'status': lambda resp: resp.status_code
    })
@tracer.start_as_current_span(name="cars_post")
def cars_post(body):  # noqa: E501
    """cars_post

    Добавления автомобиля на парковку # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = Car.from_dict(connexion.request.get_json())  # noqa: E501
    body.id = showroom.index
    showroom.Cars.append(body)
    showroom.index += 1
    logger.info(f'Добавление нового автомобиля', extra={'tags': {"car": body.id, "funcName": "cars_post", "status_code":200}})
    return "Id of a new car is " + str(body.id), '200' 
