from app import app
from app.forms import MailCreator, EditUser
from flask import render_template, redirect
from functions import get_user_info, get_users, add_user, edit_user
from functions import delete_user, domain_from_login, console_output
import config


companies = tuple(config.DOMAIN_KEY.keys())


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = MailCreator()
    if form.validate_on_submit():
        domain_data = config.DOMAIN_KEY[form.domain.data]
        resp = add_user(form.login.data, form.password.data,
                        domain_data[1], domain_data[0])
        console_output(resp, 'User creation')
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
    console_output(resp, 'User deletion')
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
    domain_data = ''
    for i in users:
        if i[0] == userid:
            print(i)
            account = i
            domain_data = config.DOMAIN_KEY[domain_from_login(i[1])]
    form = EditUser()
    form.user_id.data = account[0]
    e = form.validate_on_submit()
    print(e)
    if form.validate_on_submit():
        resp = edit_user(form.user_id.data, form.name.data,
                         form.sname.data, form.enabled.data,
                         domain_data[1], domain_data[0])
        console_output(resp, 'User editing')
        return redirect('/mails')
    form.name.data = account[2]
    form.sname.data = account[3]
    form.enabled.data = account[4]
    return render_template('edit_user.html', title='Edit user',
                           form=form, companies=companies,
                           user=account[1])


@app.route('/')
def index():
    return redirect('/mails')
