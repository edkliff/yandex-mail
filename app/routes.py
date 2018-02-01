from app import app
from app.forms import MailCreator
from flask import render_template, redirect, flash
from functions import get_user_info, get_users, add_user, del_user, response_parse
import config


companies = tuple(config.DOMAIN_KEY.keys())


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = MailCreator()
    if form.validate_on_submit():
        domain_data = config.DOMAIN_KEY[form.domain.data]
        resp = add_user(form.login.data, form.password.data, domain_data[1], domain_data[0])
        resp = response_parse(resp)
        if resp['success'] == 'ok':
            flash('User creation was finished with status {}, User: {}, UID: {}'.format(resp['success'], resp['login'],
                                                                                        resp['uid']))
        else:
            flash('User creation was finished with status {}, Error decription: {}'.format(resp['success'],
                                                                                           resp['error']))
        return redirect('/mails/{}'.format(form.domain.data))
    return render_template('new_user.html', title='New user', form=form, companies=companies)

@app.route('/mails/<domain>')
def mails(domain):
    domain_data = config.DOMAIN_KEY[domain]
    raw_users = get_users(domain_data[1], domain_data[0])
    users = get_user_info(raw_users)
    return render_template('mails.html', title='Users', users=users, domain=domain, companies=companies)


@app.route('/mails')
def all_mails():
    users = []
    for d in config.DOMAIN_KEY:
        domain_data = config.DOMAIN_KEY[d]
        raw_users = get_users(domain_data[1], domain_data[0])
        this_domain_users = get_user_info(raw_users)
        users.extend(this_domain_users)
    return render_template('mails.html', title='Users', users=users, domain='All', companies=companies)


@app.route('/delete/<domain>/<int:user_id>')
def delete_mail(user_id, domain):
    domain_data = config.DOMAIN_KEY[domain]
    resp = del_user(user_id, domain_data[1], domain_data[0])
    resp = response_parse(resp)
    if resp['success'] == 'ok':
        flash('User deletion was finished with status {}'.format(resp['success']))
    else:
        flash('User deletion was finished with status {}, Error decription: {}'.format(resp['success'], resp['error']))
    return redirect('/mails/{}'.format(domain))


@app.route('/')
def index():
    return redirect('/mails/{}'.format(companies[0]))
