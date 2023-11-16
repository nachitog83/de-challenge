from application.resources import Location, Root


def initialize_routes(api):
    api.add_resource(Root, "/")
    api.add_resource(Location, "/location")
