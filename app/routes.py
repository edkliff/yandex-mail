from app import app
from app.forms import AccountCreator, EditUser
from flask import render_template, redirect
from functions import get_users, add_user, edit_user, find_user_in_lists
from functions import delete_user, console_output
import config

# List of all companies
companies = tuple(config.DOMAIN_KEY.keys())


# New user creation
@app.route('/new', methods=['GET', 'POST'])
def new_account():
    form = AccountCreator()
    if form.validate_on_submit():
        domain_data = config.DOMAIN_KEY[form.domain.data]
        response = add_user(form.login.data, form.password.data,
                            domain_data[1], domain_data[0])
        console_output(response, 'User creation')
        return redirect('/mails/{}'.format(form.domain.data))
    return render_template('new_user.html', title='New user',
                           form=form, companies=companies)


# List of all users in domain
@app.route('/mails/<domain>')
def domain_accounts(domain):
    domain_data = config.DOMAIN_KEY[domain]
    users = get_users(domain_data[1], domain_data[0])
    return render_template('mails.html', title='{} users'.format(domain),
                           users=users, domain=domain, companies=companies)


# List of all users in all domains
@app.route('/mails')
def all_accounts():
    users = []
    for d in config.DOMAIN_KEY:
        domain_data = config.DOMAIN_KEY[d]
        this_domain_users = get_users(domain_data[1], domain_data[0])
        users.extend(this_domain_users)
    return render_template('mails.html', title='Users', users=users,
                           domain='all', companies=companies)


# User deletion
@app.route('/delete/<domain>/<int:user_id>')
def delete_account(user_id, domain):
    domain_data = config.DOMAIN_KEY[domain]
    resp = delete_user(user_id, domain_data[1], domain_data[0])
    console_output(resp, 'User deletion')
    return redirect('/mails/{}'.format(domain))


# User editing
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_account(user_id):
    users = []

    for d in config.DOMAIN_KEY:
        domain_data = config.DOMAIN_KEY[d]
        this_domain_users = get_users(domain_data[1], domain_data[0])
        users.extend(this_domain_users)
    account, domain, domain_data = find_user_in_lists(user_id, users)
    form = EditUser()
    form.user_id.data = account[0]

    if form.validate_on_submit():
        resp = edit_user(form.user_id.data, form.name.data,
                         form.sname.data, form.enabled.data,
                         domain_data[1], domain_data[0])
        console_output(resp, 'User editing')
        return redirect('/mails/{}'.format(domain))

    form.name.data = account[2]
    form.sname.data = account[3]
    form.enabled.data = account[4]
    return render_template('edit_user.html', title='Edit user',
                           form=form, companies=companies,
                           user=account[1])


@app.route('/')
def index():
    # Coming soon
    return redirect('/mails')
