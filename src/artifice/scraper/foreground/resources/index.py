from flask import current_app
from operator import attrgetter
from flask_restful import Resource

from ..utils import reply_success


class Api_Index(Resource):

    @staticmethod
    def routes_command(sort='endpoint', all_methods=False):
        """Show all registered routes with endpoints and methods.
            modified from the terminal print method in flask.cli  """
        reply = []
        rules = list(current_app.url_map.iter_rules())
        if not rules:
            return reply
        ignored_methods = set(() if all_methods else ("HEAD", "OPTIONS"))
        if sort in ("endpoint", "rule"):
            rules = sorted(rules, key=attrgetter(sort))
        rule_methods = [",".join(sorted(rule.methods - ignored_methods)) for rule in rules]
        for rule, methods in zip(rules, rule_methods):
            if (rule.endpoint != 'static') and ('dashboard' not in rule.endpoint):
                reply.append(dict(endpoint=rule.endpoint, methods=methods.split(','), rule=rule.rule))
        return reply


    def get(self):
        routes = self.routes_command()
        return reply_success(routes)
