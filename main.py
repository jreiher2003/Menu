from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

from pprint import pprint
import sqlalchemy
# pprint(sqlalchemy.__version__)


from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from database import Base, Restaurant, MenuItem

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
	restaurant = session.query(Restaurant).filter_by(id= restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'GET':
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenu(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'GET':
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=editedItem)
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenu(restaurant_id, menu_id):
	deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'GET':
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=deleteItem)
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

if __name__ == '__main__':

	app.run(debug=True)