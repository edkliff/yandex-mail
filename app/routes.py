from app import app
from app.forms import MailCreator, EditUser
from flask import render_template, redirect, flash
from functions import get_user_info, get_users, add_user, delete_user, response_parse
import config


companies = tuple(config.DOMAIN_KEY.keys())


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = MailCreator()
    if form.validate_on_submit():
        domain_data = config.DOMAIN_KEY[form.domain.data]
        resp = add_user(form.login.data, form.password.data,
                        domain_data[1], domain_data[0])
        resp = response_parse(resp)
        if resp['success'] == 'ok':
            flash('User creation was finished with status {}, User: {}, UID: {}'
                  .format(resp['success'], resp['login'], resp['uid']))
        else:
            flash('User creation was finished with status {}, Error decription: {}'
                  .format(resp['success'], resp['error']))
        return redirect('/mails/{}'.format(form.domain.data))
    return render_template('new_user.html', title='New user',
                           form=form, companies=companies)

@app.route('/mails/<domain>')
def mails(domain):
    domain_data = config.DOMAIN_KEY[domain]
    raw_users = get_users(domain_data[1], domain_data[0])
    users = get_user_info(raw_users)
    return render_template('mails.html', title='{} users'.format(domain),
                           users=users, domain=domain, companies=companies)


@app.route('/mails')
def all_mails():
    users = []
    for d in config.DOMAIN_KEY:
        domain_data = config.DOMAIN_KEY[d]
        raw_users = get_users(domain_data[1], domain_data[0])
        this_domain_users = get_user_info(raw_users)
        users.extend(this_domain_users)
    return render_template('mails.html', title='Users', users=users,
                           domain='all', companies=companies)


@app.route('/delete/<domain>/<int:user_id>')
def delete_mail(user_id, domain):
    domain_data = config.DOMAIN_KEY[domain]
    resp = delete_user(user_id, domain_data[1], domain_data[0])
    resp = response_parse(resp)
    if resp['success'] == 'ok':
        flash('User deletion was finished with status {}'.format(resp['success']))
    else:
        flash('User deletion was finished with status {}, Error decription: {}'
              .format(resp['success'], resp['error']))
    return redirect('/mails/{}'.format(domain))


@app.route('/edit/<int:userid>', methods=['GET', 'POST'])
def edit_mail(userid):
    users = []
    account = ()
    for d in config.DOMAIN_KEY:
        domain_data = config.DOMAIN_KEY[d]
        raw_users = get_users(domain_data[1], domain_data[0])
        this_domain_users = get_user_info(raw_users)
        users.extend(this_domain_users)
    for i in users:
        if i[0] == userid:
            print(i)
            account = i
    form = EditUser()
    form.user_id.data = account[0]
    form.name.data = account[2]
    form.sname.data = account[3]
    if account[4] == 'yes':
        form.enabled.data = True
    else:
        form.enabled.data = False
    if form.validate_on_submit():
        print(form.user_id.data, form.name.data,
              form.sname.data, form.enabled.data)
    return render_template('edit_user.html', title='Edit user',
                           form=form, companies=companies)


@app.route('/')
def index():
    return redirect('/mails')
