"""
Module: resources.sensor_resource

This module defines RESTful resources for managing sensor data and automation in a gardening system using Flask-RESTful.

Classes:
    - Sensor: Represents a single sensor and provides GET, DELETE, and PUT methods.
    - SensorList: Represents a list of sensors and provides GET and POST methods.
    - SensorsLast: Represents the most recent sensor data and provides a GET method.

"""

from flask import jsonify
from flask_restful import Resource, fields, marshal_with, reqparse
from models.sensors_model import SensorsModel, AutomationModel
from models import db
from utils import abort_if_doesnt_exist

# Fields for marshaling sensor data
resource_fields = {
    'id': fields.String,
    'air_temperature': fields.Float,
    'air_humidity': fields.Float,
    'luminosity': fields.Float,
    'created_at': fields.String,
    'updated_at': fields.String
}

class Sensor(Resource):
    """
    Class: Sensor

    Represents a single sensor and provides GET, DELETE, and PUT methods.

    Methods:
        - get: Retrieve sensor data by sensor ID.
        - delete: Delete sensor data by sensor ID.
        - put: Update sensor data by sensor ID.

    """
    @marshal_with(resource_fields)
    def get(self, sensor_id):
        """
        Retrieve sensor data by sensor ID.

        Parameters:
            - sensor_id (str): The ID of the sensor.

        Returns:
            - sensor (SensorsModel): The sensor data.

        """
        abort_if_doesnt_exist(SensorsModel, sensor_id)
        sensor = SensorsModel.query.filter_by(id=sensor_id).first()
        return sensor

    def delete(self, sensor_id):
        """
        Delete sensor data by sensor ID.

        Parameters:
            - sensor_id (str): The ID of the sensor.

        Returns:
            - Empty string.

        """
        abort_if_doesnt_exist(SensorsModel, sensor_id)
        sensor = SensorsModel.query.filter_by(id=sensor_id).first()
        db.session.delete(sensor)
        db.session.commit()
        return ''

    @marshal_with(resource_fields)
    def put(self, sensor_id):
        """
        Update sensor data by sensor ID.

        Parameters:
            - sensor_id (str): The ID of the sensor.

        Returns:
            - sensor (SensorsModel): The updated sensor data.

        """
        abort_if_doesnt_exist(SensorsModel, sensor_id)
        sensor = SensorsModel.query.filter_by(id=sensor_id).first()
        
        parser_update = reqparse.RequestParser()
        argument_list = [
            ('air_temperature', float, None, False),
            ('air_humidity', float, None, False),
            ('luminosity', float, None, False),
        ]
        # Iterate through the argument list and add arguments to the parser
        for arg_name, arg_type, arg_help, arg_required in argument_list:
            parser_update.add_argument(
                arg_name, 
                type=arg_type, 
                help=arg_help,
                required=arg_required
            )
        args = parser_update.parse_args()
        # Update the sensor object with non-null arguments
        for arg_name, arg_value in args.items():
            if arg_value is not None:
                setattr(sensor, arg_name, arg_value)
        db.session.commit()
        return sensor, 201


class SensorList(Resource):
    """
    Class: SensorList

    Represents a list of sensors and provides GET and POST methods.

    Methods:
        - get: Retrieve a list of all sensors.
        - post: Create a new sensor.

    """
    @marshal_with(resource_fields)
    def get(self):
        """
        Retrieve a list of all sensors.

        Returns:
            - sensors (List[SensorsModel]): A list of sensor data.

        """
        sensors = SensorsModel.query.all()
        return sensors

    def post(self):
        """
        Create a new sensor.

        Returns:
            - response (json): A JSON response containing automation updates based on new sensor values.

        """
        # Sensors values posted by the ESP32
        parser_create = reqparse.RequestParser()
        argument_list = [
            ('air_temperature', float, None, False),
            ('air_humidity', float, None, False),
            ('luminosity', float, None, False),
        ]

        # Iterate through the argument list and add arguments to the parser
        for arg_name, arg_type, arg_help, arg_required in argument_list:
            parser_create.add_argument(
                arg_name, 
                type=arg_type, 
                help=arg_help,
                required=arg_required
            )

        # Parse the incoming request arguments
        args = parser_create.parse_args()

        # Create a new sensor object with parsed arguments
        new_sensor = SensorsModel(**args)

        # Add the new sensor data to the database
        db.session.add(new_sensor)
        db.session.commit()

        # Comparing the values to the values of automation tables
        # to send a response to the esp32
        response = {}
        
        # Retrieve all automation selections from the database
        all_selection = AutomationModel.query.all()

        # Sort automation selections based on creation time in descending order
        sorted_sensors = sorted(all_selection, key=lambda all_selection: all_selection.created_at, reverse=True)
        
        # Check if there are any automation selections
        if sorted_sensors:
            # Get the latest automation selection
            last_selection = sorted_sensors[0]

        # Check if new sensor values exceed certain thresholds
        if new_sensor.air_temperature > last_selection.air_temperature_selection or \
        new_sensor.air_humidity > last_selection.air_humidity_selection:
            # Update smart plug state and timer
            extractor_plugged_timer = f"smart_plug_{last_selection.extractor_plug}_timer"
            extractor_plugged_state = f"smart_plug_{last_selection.extractor_plug}_state"
            setattr(last_selection, extractor_plugged_state, True)
            setattr(last_selection, extractor_plugged_timer, 5000)

        # Define a dictionary to map attribute names to response keys
        attribute_to_key = {
            'smart_plug_1_state': 'smart_plug_1_timer',
            'smart_plug_2_state': 'smart_plug_2_timer',
            'smart_plug_3_state': 'smart_plug_3_timer',
            'smart_plug_4_state': 'smart_plug_4_timer',
        }

        # Loop through the attributes and check if they are True
        for attribute, response_key in attribute_to_key.items():
            if getattr(last_selection, attribute):
                # Update the response dictionary with smart plug state and timer
                response[response_key] = getattr(last_selection, response_key)
                setattr(last_selection, attribute, False)
        
        # Commit the changes to the database
        db.session.add(last_selection)
        db.session.commit()

        return jsonify(response)

class SensorsLast(Resource):
    """
    Class: SensorsLast

    Represents the most recent sensor data and provides a GET method.

    Methods:
        - get: Retrieve the most recent sensor data.

    """
    @marshal_with(resource_fields)
    def get(self):
        """
        Retrieve the most recent sensor data.

        Returns:
            - most_recent_sensor (SensorsModel): The most recent sensor data.

        """
        most_recent_sensor = SensorsModel.query.order_by(SensorsModel.created_at.desc()).first()
        return most_recent_sensor
