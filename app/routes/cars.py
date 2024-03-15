from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Car, Comment
from app.classes.forms import CarForm, CommentForm
from flask_login import login_required
import datetime as dt

@app.route('/car/new', methods=['GET', 'POST'])
@login_required
def carNew():
    form = CarForm()
    if form.validate_on_submit():
        newCar = Car(
            manufacturer = form.manufacturer.data,
            type = form.type.data,
            model = form.model.data,
            year = form.year.data,
            image = form.image.data,
            engine = form.engine.data,
            gas = form.gas.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow
        )
        newCar.save()
        return redirect(url_for('car',blogID=newCar.id))
    return render_template('carform.html',form=form)