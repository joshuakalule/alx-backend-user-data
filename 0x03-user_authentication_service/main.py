#!/usr/bin/env python3
"""
Main file
"""
import requests

URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """Assert correct results for register user"""
    url = URL + '/users'
    data = {
        'email': email,
        'password': password
    }
    r = requests.post(url, data=data)

    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """test wrong password login"""
    url = URL + '/sessions'
    data = {
        'email': email,
        'password': password
    }
    r = requests.post(url, data=data)

    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """assert valid log in"""
    url = URL + '/sessions'
    data = {
        'email': email,
        'password': password
    }
    r = requests.post(url, data=data)

    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    session_id = r.cookies.get('session_id')
    assert session_id

    return session_id


def profile_unlogged() -> None:
    """test access to profile with no session id"""
    url = URL + '/profile'

    r = requests.get(url)

    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """test authorized access to profile"""
    url = URL + '/profile'
    cookies = dict(session_id=session_id)

    r = requests.get(url, cookies=cookies)

    assert r.status_code == 200
    assert type(r.json()) == dict


def log_out(session_id: str) -> None:
    """test successful logout"""
    url = URL + '/sessions'
    cookies = dict(session_id=session_id)

    r = requests.delete(url, cookies=cookies)

    assert r.status_code == 200  # should succeed
    assert r.history  # should not be empty as there is a redirect
    assert r.json() == {'message': 'Bienvenue'}  # response from redirect


def reset_password_token(email: str) -> str:
    """assert get reset token"""
    url = URL + '/reset_password'
    data = {'email': email}

    r = requests.post(url, data=data)

    assert r.status_code == 200
    assert r.json()

    reset_token = r.json().get('reset_token')
    assert reset_token

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test reset password"""
    url = URL + '/reset_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    r = requests.put(url, data=data)

    assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
