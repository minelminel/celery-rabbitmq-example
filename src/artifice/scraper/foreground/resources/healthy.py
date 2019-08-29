from flask_restful import Resource

from ..utils import reply_success


class Api_Healthy(Resource):

    def get(self):
        return reply_success()
