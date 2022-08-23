from flask import Flask, jsonify, request, abort
from models import setup_db, Plant


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/plants', methods=['GET', 'POST'])
    def get_plants():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 1
        end = start + 1

        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants': formatted_plants[start:end],
            'total_plants': len(formatted_plants)
        })

    @app.route('/plants/<int:plant_id>')
    def get_individual_plant(plant_id):
        # this will query and filter he plants
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()
        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'plant': plant.format()
            })
    return app
