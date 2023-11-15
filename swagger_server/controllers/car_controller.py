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

car_counter = metrics.counter(
    'cnt_car', 'Number of invocations per car', labels={
        'car': lambda: request.view_args['carId']
    })

@car_counter
def cars_car_id_delete(car_id):  # noqa: E501
    """cars_car_id_delete

    Получение информации о госте по номеру # noqa: E501

    :param car_id: 
    :type car_id: int

    :rtype: None
    """
    for car in showroom.Cars:
        if car._id == car_id:
            showroom.Cars.remove(car)
            return '200'
    return '400'

@car_counter
def cars_car_id_get(car_id):  # noqa: E501
    """cars_car_id_get

    Получение информации о госте по номеру # noqa: E501

    :param car_id: 
    :type car_id: int

    :rtype: Car
    """
    for car in showroom.Cars:
        if car._id == car_id:
            return car.to_dict(), '200'
    return '400'

@car_counter
def cars_car_id_put(car_id, body=None):  # noqa: E501
    """Обновление автомобиля

    Изменение информации об автомобиле по номеру id # noqa: E501

    :param car_id: 
    :type car_id: int
    :param body: 
    :type body: dict | bytes

    :rtype: Car
    """
    if connexion.request.is_json:
        body = Car.from_dict(connexion.request.get_json())  # noqa: E501
    for i in range(len(showroom.Cars)):
        if (showroom.Cars[i]._id == car_id):
            body.id = car_id
            showroom.Cars[i] = body
            return '200'
    return '400'

@metrics.summary('get_duration_seconds_sum', 'Get request latencies',
                 labels={'status': lambda r: r.status_code})
@metrics.gauge('get_in_progress', 'Long running requests in progress')
def cars_get():  # noqa: E501
    """cars_get

    Получение списка автомобилей в автосалоне # noqa: E501

    :rtype: List[Car]
    """
    time.sleep(10)
    return jsonify(showroom.Cars), '200'

@metrics.counter('cnt_post', 'Number of invocations cars post', labels={
        'status': lambda resp: resp.status_code
    })
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
    return "Id of a new car is " + str(body.id), '200' 
