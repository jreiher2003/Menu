from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/restaurants')
def main():
	return render_template('base.html')

@app.route('/restaurant/new')
def createNew():
	return 'create new restaurant'

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	return 'Edit restaurant'

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	return 'Delete restaurant'

@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
	return 'Menu of restaurant'

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	return 'Create New menu Item'

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenu(restaurant_id, menu_id):
	return 'Edit a menu item'

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenu(restaurant_id, menu_id):
	return 'Delete a menu item'


if __name__ == '__main__':

	app.run(debug=True)