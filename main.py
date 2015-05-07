from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

from pprint import pprint
import sqlalchemy
# pprint(sqlalchemy.__version__)


from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from database import Base, Restaurant

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def main():
	restaurant = session.query(Restaurant).all()		
	return render_template('front.html', restaurant=restaurant)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def createNew():
	if request.method == 'GET':
		return render_template('newrestaurant.html')
		
	if request.method == 'POST':
		newRest = Restaurant(name= request.form['name'])
		session.add(newRest)
		session.commit()
		return redirect(url_for('main'))


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'GET':
		return render_template('editrestaurant.html', restaurant_id=restaurant_id, r=editedRestaurant)
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
			session.add(editedRestaurant)
			session.commit()
			return redirect(url_for('main'))

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'GET':
		return render_template('deleterestaurant.html', restaurant_id=restaurant_id, r=deletedRestaurant)
	if request.method == 'POST':
		session.delete(deletedRestaurant)
		session.commit()
		return redirect(url_for('main'))


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