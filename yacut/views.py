from random import choices
from string import ascii_letters, digits

from flask import flash, redirect, render_template, request

from . import app, db
from .constants import NUMBER_CHARACTERS
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    return ''.join(
        choices(ascii_letters + digits, k=NUMBER_CHARACTERS)
    )


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id == '' or custom_id is None:
            custom_id = get_unique_short_id()
        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!', 'error')
            return render_template('index.html', form=form)
        new_url = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(new_url)
        db.session.commit()
        new_url_adress = request.host_url + custom_id
        flash(
            f'Ваша новая ссылка готова: "<a href="{new_url_adress}">{new_url_adress}</a>"',
            'info'
        )
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<short>')
def original_link_to(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)
