"""
Module: resources.automation_resource

This module defines RESTful resources for managing automation settings in a gardening system using Flask-RESTful.

Classes:
    - AutomationList: Represents a list of automation settings and provides GET and POST methods.

"""

from flask import jsonify
from flask_restful import Resource, fields, marshal_with, reqparse
from models import db
from utils import abort_if_doesnt_exist
from models.sensors_model import AutomationModel

# Fields for marshaling automation settings
resource_fields = {
    'id': fields.String,
    'air_humidity_selection': fields.Integer,
    'air_temperature_selection': fields.Integer,
    'extractor_plug': fields.Integer,
    'smart_plug_1_state': fields.Boolean,
    'smart_plug_1_timer': fields.Integer,
    'smart_plug_2_state': fields.Boolean,
    'smart_plug_2_timer': fields.Integer,
    'smart_plug_3_state': fields.Boolean,
    'smart_plug_3_timer': fields.Integer,
    'smart_plug_4_state': fields.Boolean,
    'smart_plug_4_timer': fields.Integer
}

class AutomationList(Resource):
    """
    Class: AutomationList

    Represents a list of automation settings and provides GET and POST methods.

    Methods:
        - get: Retrieve a list of all automation settings.
        - post: Create a new automation setting.

    """
    @marshal_with(resource_fields)
    def get(self):
        """
        Retrieve a list of all automation settings.

        Returns:
            - selections (List[AutomationModel]): A list of automation settings.

        """
        selections = AutomationModel.query.all()
        return selections

    @marshal_with(resource_fields)
    def post(self):
        """
        Create a new automation setting.

        Returns:
            - new_selection (AutomationModel): The newly created automation setting.

        """
        parser_create = reqparse.RequestParser()

        # Define a list of argument names and their types
        argument_list = [
            ('air_humidity_selection', int, None, False),
            ('air_temperature_selection', int, None, False),
            ('extractor_plug', int, None, False),
            ('smart_plug_1_state', bool, None, False),
            ('smart_plug_1_timer', int, None, False),
            ('smart_plug_2_state', bool, None, False),
            ('smart_plug_2_timer', int, None, False),
            ('smart_plug_3_state', bool, None, False),
            ('smart_plug_3_timer', int, None, False),
            ('smart_plug_4_state', int, None, False),
            ('smart_plug_4_timer', int, None, False)
        ]

        # Iterate through the argument list and add arguments to the parser
        for arg_name, arg_type, arg_help, arg_required in argument_list:
            parser_create.add_argument(
                arg_name, 
                type=arg_type, 
                help=arg_help,
                required=arg_required
            )

        args = parser_create.parse_args()

        # Create the AutomationModel object using the arguments
        new_selection = AutomationModel(**args)
        
        db.session.add(new_selection)
        db.session.commit()
        
        return new_selection, 201
