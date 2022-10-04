from flask import Flask, jsonify, request, make_response, abort, request, render_template
import datetime 
from datetime import date
app = Flask(__name__)
import recipe_list.py

#<------------------ GLOBAL Recipes list[] which store all of the JSON objects which we use to render make reqquests via HTTP methods------------------>
# We could initialize this with an empty array 
recipes = [
      {'id': 0, 
       'name': 'Picante de Pollo',
       'ingredients': ['Chicken','Onions', 'tomatos','black-pepper','salt','garlic'],
       'instructions': 'Boil 2lbs of chicken (breats, thighs or legs) preferably on the bone.',
       'serving size': 12,
       'category': 'Latin',
       'notes': 'Notes entry test',
       'date-added': '2022-10-03',
       'date-modified': 'none'}
]

def view_recipes():
    cur_recipes = recipes
    return cur_recipes

@app.route('/recipes/list_view',methods=['GET', 'POST'])
def index():
    return render_template('index2.html', list_recipes= cur_recipes) #jsonify({'recipes':recipes}))


#<-------------------------------------GET MTHODS------------------------------------------>
@app.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify({'recipes':recipes})

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = [recipe for recipe in recipes if recipe['id'] == recipe_id]
    if len(recipe) == 0:
        abort(404) #bad request
    return jsonify({'recipe':recipe[0]})



#<-------------------------------------ERROR HANDLING---------------------------------->
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error: please review your request and resubmit'}), 404)




#<-------------------------------POST METHODS------------------------->
@app.route('/recipes', methods=['POST'])
def add_recipe():
    if not request.json or not 'name' in request.json:
        abort('400')
    recipe ={'id': recipes[-1]['id']+1,
            'name': request.json['name'],
            'ingredients': request.json['ingredients'],
            'instructions': request.json['instructions'],
            'serving size': request.json['serving size'],
            'category': request.json['category'],
            'notes': request.json['notes'],
            'date-added': date.today(),
            'date-modified': 'none'
            }
    recipes.append(recipe)
    #recipes.append(request.get_json()), 
    return jsonify({'recipe':recipe}), 201

#<---------------------------------------PUT METHODS (Modify)--------------------------------------->
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def modify_recipe(recipe_id):
    recipe = [recipe for recipe in recipes if recipe['id'] == recipe_id]
    if len(recipe) ==0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    if'instructions' in request.json and type(request.json['instructions']) is not str:
        abort(400)
    if 'serving size' in request.json and type(request.json['serving size']) is not int:
        abort(400)
    recipe[0]['name'] =  request.json.get('name', recipe[0]['name'])
    recipe[0]['ingredients'] = request.json.get('ingredients',recipe[0]['ingredients'])
    recipe[0]['instructions'] = request.json.get('instructions',recipe[0]['instructions'])
    recipe[0]['serving size'] = request.json.get('serving size',recipe[0]['serving size'])
    return jsonify({'recipe':recipe[0]})

#<--------------------------------------DELETE METHODS-------------------------------------------->
@app.route("/recipes/<int:recipe_id>", methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = [recipe for recipe in recipes if recipe['id'] == recipe_id]
    if len(recipe) == 0:
        abort(404)
    recipes.remove(recipe[0])
    return jsonify({'result':'Success! The recipe specified was removed.'})

