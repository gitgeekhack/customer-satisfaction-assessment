from flask import jsonify, make_response
from app.resource.main_app import flask_app
from app.manage import create_app
from app.resource.common import common_app

app, logger = create_app(debug=True)
app.register_blueprint(common_app)
app.register_blueprint(flask_app)


@app.errorhandler(404)
def page_not_found(e):
    """Default 404 handler"""
    return make_response(jsonify(ErrorMessage="Not found"), 404)
