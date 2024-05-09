from matplotlib import image
import mongoengine.errors
from app import app
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Car
from app.classes.forms import CarForm
from flask_login import login_required
import datetime as dt

@app.route('/viewall')
@login_required
def carList():
    cars = Car.objects()
    return render_template('carsview.html',cars=cars)

@app.route('/car/new', methods=['GET', 'POST'])
@login_required
def carNew():
    form = CarForm()

    if form.validate_on_submit():

        newCar = Car(
            manufacturer = form.manufacturer.data,
            recurring = form.recurring.data,
            model = form.model.data,
            year = form.year.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow

        )
        newCar.save()

        return redirect(url_for('car',carID=newCar.id))

    return render_template('carform.html',form=form)

@app.route('/car/edit/<carID>', methods=['GET', 'POST'])
@login_required
def carEdit(carID):
    editCar = Car.objects.get(id=carID)

    if current_user != editCar.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('car',carID=carID))

    form = CarForm()
    if form.validate_on_submit():
        editCar.update(
            manufacturer = form.manufacturer.data,
            recurring = form.recurring.data,
            model = form.model.data,
            year = form.year.data,
            modify_date = dt.datetime.utcnow,
        )
        return redirect(url_for('car',carID=carID))

    form.manufacturer.data = editCar.manufacturer
    form.recurring.data = editCar.recurring
    form.model.data = editCar.model
    form.year.data = editCar.year

    return render_template('carform.html',form=form)


@app.route('/car/<carID>/')
@login_required
def car(carID):
    thisCar = Car.objects.get(id=carID)
    return render_template('car.html',car=thisCar)

@app.route('/car/delete/<carID>')
@login_required
def carDelete(carID):
    deleteCar = Car.objects.get(id=carID)

    deleteCar.delete()
    flash('The Log was deleted.')
    return redirect(url_for('carList'))
