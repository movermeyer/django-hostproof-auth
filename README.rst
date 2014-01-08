django-hostproof-auth
======================

.. image:: https://travis-ci.org/jpintado/django-hostproof-auth.png?branch=master
    :target: https://travis-ci.org/jpintado/django-hostproof-auth

Secure Host-Proof authentication backend for Django-powered sites.

The password is never transmitted to the server. The server is limited to persisting and retrieving whatever encrypted data is sent to it, and never actually accesses the sensitive data in its plain form.

Installation
============

Install package
---------------

- Clone the repository::

    git clone https://github.com/jpintado/django-hostproof-auth.git

- Install the package::

    python setup.py install

You could require root permissions to execute the previous command.
    

Configuration
-----------

- Add ``hostproof_auth`` to ``INSTALLED_APPS``.

- Add the authentication backend to your application::

    AUTH_USER_MODEL = 'hostproof_auth.User'

    AUTHENTICATION_BACKENDS = (
        'hostproof_auth.auth.ModelBackend',
    )

Usage
=====

Registration
------------

- POST request to the ``hostproof_auth_register`` URL (typically something like */register/*) with the parameters:

  - username
  - email
  - encrypted_challenge
  - challenge
  
  The client application needs to generate a random string as challenge, and encrypt that string using a secure algorith (for example, AES-256) with the user password to generate the encrypted challenge.

  Example::
  
    username=foobar&email=foobar@domain.com&challenge=randomstring&encrypted_challenge=U2FsdGVkX19ED2i2M8uE3AySNJyKzw8SXtru9JQbNmo=

Login
-----

- GET request to the ``challenge`` URL (typically something like */challenge/*) with the parameter ``username``.

  Example::
  
    /challenge/?username=foobar

  Response::
  
    {
      "encrypted_challenge" : "U2FsdGVkX19ED2i2M8uE3AySNJyKzw8SXtru9JQbNmo="
    }
    
- POST request to the ``challenge`` URL with the parameter ``username`` and ``challenge``.

  The client application needs to decrypt the encrypted_challenge using the password, and send the original challenge as response to be authenticated.
  
  Example::

    username=foobar&challenge=randomstring

 
