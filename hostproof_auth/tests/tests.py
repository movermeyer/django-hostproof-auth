from django.test import TestCase
from django.test import Client
from django.db import IntegrityError

from hostproof_auth.models import *

import json


class UserCreationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="john",
                    email="john.smith@domain.com",
                    challenge="randomstring",
                    encrypted_challenge="encryptedrandomstring")

    def test_duplicated_pk_creation(self):
        try:
            User.objects.create_user(username="john",
                    email="different.email@domain.com",
                    challenge="randomstring",
                    encrypted_challenge="encryptedrandomstring")
            self.fail("User created with duplicated pk")
        except IntegrityError:
            pass

class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="john",
                        email="john.smith@domain.com",
                        challenge="randomstring",
                        encrypted_challenge="encryptedrandomstring")

    def test_get_register(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 405)

    def test_post_register_invalid_parameters(self):
        response = self.client.post("/register/")
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/register/", {"email":"leeroy@domain.com",
                                    "challenge":"randomstring",
                                    "encrypted_challenge":"encryptedrandomstring"})
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/register/", {"username":"leeroy.jenkins",
                                    "challenge":"randomstring",
                                    "encrypted_challenge":"encryptedrandomstring"})
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/register/", {"username":"leeroy.jenkins",
                                    "email":"leeroy@domain.com",
                                    "encrypted_challenge":"encryptedrandomstring"})
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/register/", {"username":"leeroy.jenkins",
                                    "email":"leeroy@domain.com",
                                    "challenge":"randomstring"})
        self.assertEqual(response.status_code, 400)

    def test_post_register_valid_parameters(self):
        response = self.client.post("/register/", {"username":"leeroy.jenkins",
                                    "email":"leeroy@domain.com",
                                    "challenge":"randomstring",
                                    "encrypted_challenge":"encryptedrandomstring"})
        self.assertEqual(response.status_code, 200)

    def test_post_register_duplicated_username(self):
        response = self.client.post("/register/", {"username":"john",
                                    "email":"otheremail@domain.com",
                                    "challenge":"randomstring",
                                    "encrypted_challenge":"encryptedrandomstring"})
        self.assertEqual(response.status_code, 409)
    def test_post_register_duplicated_username(self):
        response = self.client.post("/register/", {"username":"different.username",
                                    "email":"john.smith@domain.com",
                                    "challenge":"randomstring",
                                    "encrypted_challenge":"encryptedrandomstring"})
        self.assertEqual(response.status_code, 409)

class ChallengeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="john",
                        email="john.smith@domain.com",
                        challenge="randomstring",
                        encrypted_challenge="encryptedrandomstring")

    def test_get_challenge_invalid_parameters(self):
        response = self.client.get("/challenge/")
        self.assertEqual(response.status_code, 400)

    def test_get_challenge_invalid_username(self):
        response = self.client.get("/challenge/", {"username":"invalidusername"})
        self.assertEqual(response.status_code, 404)

    def test_get_challenge_valid_username(self):
        response = self.client.get("/challenge/", {"username":"john"})
        self.assertEqual(response.status_code, 200)

    def test_get_challenge_valid_json(self):
        response = self.client.get("/challenge/", {"username":"john"})
        try:
            json.loads(response.content.decode('utf-8'))
        except ValueError:
            self.fail("Bad JSON format")

    def test_get_challenge_valid_encrypted_challenge(self):
        response = self.client.get("/challenge/", {"username":"john"})
        try:
            challenge_json = json.loads(response.content.decode('utf-8'))
            self.assertEqual("encrypted_challenge" in challenge_json, True)
            self.assertEqual(challenge_json["encrypted_challenge"], "encryptedrandomstring")
        except ValueError:
            self.fail("Bad JSON format")

    def test_post_challenge_invalid_parameters(self):
        response = self.client.post("/challenge/")
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/challenge/", {"username":"john"})
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/challenge/", {"challenge":"randomstring"})
        self.assertEqual(response.status_code, 400)

    def test_post_challenge_valid_parameters(self):
        response = self.client.post("/challenge/", {"username":"john", "challenge":"randomstring"})
        self.assertEqual(response.status_code, 200)

    def test_get_challenge_valid_json(self):
        response = self.client.post("/challenge/", {"username":"john", "challenge":"randomstring"})
        try:
            rsa_json = json.loads(response.content.decode('utf-8'))
            self.assertEqual("rsa_public" in rsa_json, True)
        except ValueError:
            self.fail("Bad JSON format")
