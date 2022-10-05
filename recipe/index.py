from flask import Flask, jsonify, request, make_response, abort, request, render_template
import datetime 
from datetime import date
app = Flask(__name__)

#<------------------ GLOBAL Recipes list[] which store all of the JSON objects which we use to render make reqquests via HTTP methods------------------>
# We could initialize this with an empty array if we wanted to strat with no recipes
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

@app.route('/recipes/list_view',methods=['GET', 'POST'])
def list_view():
    list_1 = ['test','test2','test3','test4'] 
        
    return render_template('index.html', list_view=recipes) #jsonify({'recipes':recipes}))


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
# Key to this function is that we incriment the 'id' tag by +1 for everytime we post a new recipe:
#   -->implemtation for auto-updating id-field in JSON obj in restful fasion  without use of a database
# returns a single 'recipe' JSON object with status code 201 successful 
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
# Key here is that we specify the unique 'id' in the route
#   --> Then take a new list and set the value of new_list[0] to the value of the JSON object that has position of unique 'id' in the global var recipies list: recipes['id']
# returns a single modified recipe JSON obj stored in a list similar to our Global-var recipes[] list
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def modify_recipe(recipe_id):
    recipe = [recipe for recipe in recipes if recipe['id'] == recipe_id] # [x] for i in recipes if recipe[id] == <recipie_id>
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
    if 'category' in request.json and type(request.json['category']) is not str:
        abort(400)
    if 'notes' in request.json and type(request.json['notes']) is not str:
        abort(400)
    if 'date-added' in request.json and type(request.json['notes']) is not str:
        abort(400)
    recipe[0]['name'] =  request.json.get('name', recipe[0]['name'])
    recipe[0]['ingredients'] = request.json.get('ingredients',recipe[0]['ingredients'])
    recipe[0]['instructions'] = request.json.get('instructions',recipe[0]['instructions'])
    recipe[0]['serving size'] = request.json.get('serving size',recipe[0]['serving size'])
    recipe[0]['category'] = request.json.get('category',recipe[0]['category'])
    recipe[0]['notes'] = request.json.get('notes',recipe[0]['notes'])
    recipe[0]['date-added'] = request.json.get('date-added',recipe[0]['date-added'])
    recipe[0]['date-modified'] = request.json.get('date-modified',date.today())
    return jsonify({'recipe':recipe[0]})

#<--------------------------------------DELETE METHODS-------------------------------------------->
@app.route("/recipes/<int:recipe_id>", methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = [recipe for recipe in recipes if recipe['id'] == recipe_id]
    if len(recipe) == 0:
        abort(404)
    recipes.remove(recipe[0])
    return jsonify({'result':'Success! The recipe specified was removed.'})
