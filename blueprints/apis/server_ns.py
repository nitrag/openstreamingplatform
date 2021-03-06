from flask_restplus import Api, Resource, reqparse, Namespace

from classes import settings
from classes.shared import db

api = Namespace('server', description='Server Related Queries and Functions')

@api.route('/')
class api_1_Server(Resource):
    # Server - Get Basic Server Information
    def get(self):
        """
            Displays a Listing of Server Settings
        """
        serverSettings = settings.settings.query.all()[0]
        db.session.commit()
        return {'results': serverSettings.serialize() }


@api.route('/edges')
class api_1_Edges(Resource):
    # Server - Get Edge Serves
    def get(self):
        """
            Displays a Listing of Edge Servers
        """

        edgeList = settings.edgeStreamer.query.all()
        db.session.commit()
        return {'results': [ob.serialize() for ob in edgeList]}