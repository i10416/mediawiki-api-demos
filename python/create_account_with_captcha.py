#!/usr/bin/python3

"""
    create_account_with_captcha.py

    MediaWiki Action API Code Samples
    Demo of `createaccount` module: Create an account on a wiki with a special
    authentication extension installed. This example considers a case of a wiki
    where captcha is enabled through extensions like ConfirmEdit
    (https://www.mediawiki.org/wiki/Extension:ConfirmEdit)

    This demo app uses Flask (a Python web development framework).

    MIT license
"""

import requests
from flask import Flask, render_template, flash, request

S = requests.Session()
TEST_WIKI_URL = "https://test.wikipedia.org"
TEST_API_ENDPOINT = TEST_WIKI_URL + "/w/api.php"

MEDIA_WIKI_URL = "https://test.wikipedia.org"
MEDIA_API_ENDPOINT = MEDIA_WIKI_URL + "/w/api.php"

# App config.
DEBUG = True
APP = Flask(__name__)
APP.config.from_object(__name__)
APP.config['SECRET_KEY'] = 'enter_your_secret_key'


@APP.route("/", methods=['GET', 'POST'])
def show_form():
    """ Render form template and handle form submission request """

    captcha_fields = get_captcha_fields()
    captcha_url = TEST_WIKI_URL + captcha_fields['captchaInfo']['value']


    if request.method == 'POST':
        details = {
            'name': request.form['username'],
            'password': request.form['password'],
            'confirm_password': request.form['retype'],
            'email': request.form['email'],
            'captcha_word': request.form['captcha-word'],
            'captcha_id': captcha_fields['captchaId']['value']
        }

        create_account(details)
    
    register_fields = list()
    registration_fields = get_registration_fields()
    for x in registration_fields:
        field = {
            'name': x,
            'type': registration_fields[x]['type'],
            'label': registration_fields[x]['label'],
        }
        register_fields.append(field)
    register_fields.append({
        'name': 'captcha-word',
        'type': 'text',
        'label': 'Enter the text you see on the image below'
        })

    return render_template(
        'create_account_form.html',
        captcha=captcha_url,
        fields=register_fields
    )


def get_captcha_fields():
    """ Fetch the captcha fields from `authmanagerinfo` module """

    response = S.get(
        url=TEST_API_ENDPOINT,
        params={
            'action': 'query',
            'meta': 'authmanagerinfo',
            'amirequestsfor': 'create',
            'format': 'json'})

    data = response.json()
    query = data and data['query']
    authmanagerinfo = query and query['authmanagerinfo']
    fields = authmanagerinfo and authmanagerinfo['requests']

    for k in fields:
        if k['account'] == 'CaptchaAuthenticationRequest':
            return k and k['fields']
    return None


def get_registration_fields():
    """ Fetch the registration form fields from `authmanagerinfo` module """

    response = S.get(
        url=MEDIA_API_ENDPOINT,
        params={
            'action': 'query',
            'meta': 'authmanagerinfo',
            'amirequestsfor': 'create',
            'format': 'json'})

    data = response.json()
    query = data and data['query']
    authmanagerinfo = query and query['authmanagerinfo']
    fields = authmanagerinfo and authmanagerinfo['requests']

    ret_field = dict()

    for k in fields:
        if k['id'] == 'MediaWiki\\Auth\\PasswordAuthenticationRequest' or k['id'] == 'MediaWiki\\Auth\\UserDataAuthenticationRequest':
            k_field = k and k['fields']
            for x in k_field:
                ret_field[x] = k_field[x]
    if not ret_field:
        return None
    return ret_field


def create_account(details):
    """ Send a post request along with create account token, user information
    and return URL to the API to create an account on a wiki """

    createtoken = fetch_create_token()

    response = S.post(url=TEST_API_ENDPOINT, data={
        'action': 'createaccount',
        'createtoken': createtoken,
        'username': details['name'],
        'password': details['password'],
        'retype': details['confirm_password'],
        'email': details['email'],
        'createreturnurl': 'http://127.0.0.1:5000/',
        'captchaId': details['captcha_id'],
        'captchaWord': details['captcha_word'],
        'format': 'json',
    })

    data = response.json()
    print (data)
    createaccount = data['createaccount']

    if createaccount['status'] == "PASS":
        flash(
            'Success! An account with username ' + details['name'] + ' has been created!')
    else:
        flash(
            'Oops! Something went wrong -- ' + createaccount['messagecode'] + "." +
            createaccount['message'])


def fetch_create_token():
    """ Fetch create account token via `tokens` module """

    response = S.get(
        url=TEST_API_ENDPOINT,
        params={
            'action': 'query',
            'meta': 'tokens',
            'type': 'createaccount',
            'format': 'json', })

    data = response.json()
    return data['query']['tokens']['createaccounttoken']


if __name__ == "__main__":
    APP.run()
