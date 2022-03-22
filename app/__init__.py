from flask import jsonify, make_response
from app.resource.sentiment_analysis_app import sentiment_analysis
from app.manage import create_app
from app.resource.common import common_app

app, logger = create_app(debug=False)
app.register_blueprint(common_app)
app.register_blueprint(sentiment_analysis)


@app.errorhandler(404)
def page_not_found(e):
    """Default 404 handler"""
    return make_response(jsonify(ErrorMessage="Not found"), 404)
