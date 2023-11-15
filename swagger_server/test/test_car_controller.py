# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.car import Car  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCarController(BaseTestCase):
    """CarController integration test stubs"""

    def test_cars_car_id_delete(self):
        """Test case for cars_car_id_delete

        
        """
        response = self.client.open(
            '/cars/{carId}'.format(car_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cars_car_id_get(self):
        """Test case for cars_car_id_get

        
        """
        response = self.client.open(
            '/cars/{carId}'.format(car_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cars_car_id_put(self):
        """Test case for cars_car_id_put

        Обновление автомобиля
        """
        body = Car()
        response = self.client.open(
            '/cars/{carId}'.format(car_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cars_get(self):
        """Test case for cars_get

        
        """
        response = self.client.open(
            '/cars',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cars_post(self):
        """Test case for cars_post

        
        """
        body = Car()
        response = self.client.open(
            '/cars',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
