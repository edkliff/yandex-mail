from app import app
from app.forms import AccountCreator, EditUser
from flask import render_template, redirect
from app.functions import get_users, add_user, edit_user, find_user_in_lists
from app.functions import delete_user, console_output
import config


# List of all companies
companies = tuple(config.DOMAIN_KEY.keys())


# New user creation
@app.route('/new', methods=['GET', 'POST'])
def new_account():
    """
    New user account
    :form: AccountCreator
    :return: New user form or redirect to domain list
    """
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
    """
    List accounts on domain
    :param domain: domain for listing
    :return: domain accounts list page
    """
    domain_data = config.DOMAIN_KEY[domain]
    users = get_users(domain_data[1], domain_data[0])
    return render_template('mails.html', title='{} users'.format(domain),
                           users=users, domain=domain, companies=companies)


# List of all users in all domains
@app.route('/mails')
def all_accounts():
    """
    List all accounts on all domains
    :return: accounts list page
    """
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
    """
    Delete user
    :param user_id: user_id for deletion
    :param domain: domain for user
    :return: domain accounts list page
    """
    domain_data = config.DOMAIN_KEY[domain]
    resp = delete_user(user_id, domain_data[1], domain_data[0])
    console_output(resp, 'User deletion')
    return redirect('/mails/{}'.format(domain))


# User editing
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_account(user_id):
    """
    User editing
    :param user_id: user_id for editing
    :return: domain accounts list page
    """
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
                         domain_data[1], domain_data[0],
                         form.birth_date.data, form.sex.data,
                         form.hintq.data, form.hinta.data)
        console_output(resp, 'User editing')
        print(form.birth_date.data, form.user_id.data, form.name.data,
              form.sname.data, form.enabled.data,
              domain_data[1], domain_data[0], form.birth_date.data,
              form.sex.data, form.hintq.data, form.hinta.data)
        return redirect('/mails/{}'.format(domain))

    form.name.data = account[2]
    form.sname.data = account[3]
    form.enabled.data = account[4]
    form.birth_date.data = account[6]
    form.sex.data = str(account[7])
    form.hintq.data = account[8]
    form.hinta.data = account[9]
    print(form.birth_date.data, form.user_id.data, form.name.data,
          form.sname.data, form.enabled.data,
          domain_data[1], domain_data[0], form.birth_date.data,
          form.sex.data, form.hintq.data, form.hinta.data)
    return render_template('edit_user.html', title='Edit user',
                           form=form, companies=companies,
                           user=account[1])


# Logs
@app.route('/messages')
def messages():
    """
    Logs
    :return: list of logs
    """
    return render_template('messages.html', title='Messages',
                           domain='all', companies=companies)


@app.route('/')
def index():
    # Coming soon
    return redirect('/mails')
