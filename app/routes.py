from app import app
from app.forms import MailCreator
from flask import render_template, redirect, flash
from functions import get_user_info, get_users, add_user, del_user
import config


companies = config.DOMAIN_KEY.keys()


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = MailCreator()
    print(form.login.data, form.password.data, form.domain.data)
    if form.validate_on_submit():
        domain_data = config.DOMAIN_KEY[form.domain.data]
        print(form.login.data, form.password.data, form.domain.data,
              domain_data[1], domain_data[0])
        resp = add_user(form.login.data, form.password.data, domain_data[1], domain_data[0])
        print(resp)
        return redirect('/mails/{}'.format(form.domain.data))
    print(form.validate_on_submit())
    return render_template('new_user.html', title='New user', form=form, companies=companies)

@app.route('/mails/<domain>')
def mails(domain):
    domain_data = config.DOMAIN_KEY[domain]
    raw_users = get_users(domain_data[1], domain_data[0])
    users = get_user_info(raw_users)
    return render_template('mails.html', title='Users', users=users, domain=domain, companies=companies)


@app.route('/delete/<domain>/<int:user_id>')
def delete_mail(user_id, domain):
    domain_data = config.DOMAIN_KEY[domain]
    del_user(user_id, domain_data[1], domain_data[0])
    return redirect('/mails/{}'.format(domain))


@app.route('/')
def index():
    return redirect('/new')