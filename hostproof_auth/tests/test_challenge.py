from django.test import TestCase
from django.test import Client
from django.db import IntegrityError

from hostproof_auth.models import *

import json


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
        response = self.client.get("/challenge/", {"username":"john", 'format':'json'})
        try:
            json.loads(response.content)
        except ValueError:
            self.fail("Bad JSON format")

    def test_get_challenge_invalid_format(self):
        response = self.client.get("/challenge/", {"username":"john", 'format':'invalidformat'})
        self.assertEqual(response.status_code, 400)


    def test_get_challenge_valid_encrypted_challenge(self):
        response = self.client.get("/challenge/", {"username":"john", 'format':'json'})
        try:
            challenge_json = json.loads(response.content)
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
        response = self.client.post("/challenge/", {"username":"john", "challenge":"randomstring", 'format':'json'})
        try:
            rsa_json = json.loads(response.content)
            self.assertEqual("rsa_public" in rsa_json, True)
        except ValueError:
            self.fail("Bad JSON format")

    def test_post_challenge_invalid_format(self):
        response = self.client.post("/challenge/", {"username":"john", "challenge":"randomstring", "format":"invalidformat"})
        self.assertEqual(response.status_code, 400)

    def test_post_challenge_invalid_credentials(self):
        response = self.client.post("/challenge/", {"username":"john", "challenge":"invalidchallenge"})
        self.assertEqual(response.status_code, 403)

    def test_challenge_invalid_methods(self):
        response = self.client.head("/challenge/")
        self.assertEqual(response.status_code, 405)
        response = self.client.options("/challenge/", {})
        self.assertEqual(response.status_code, 405)
        response = self.client.put("/challenge/", {})
        self.assertEqual(response.status_code, 405)
        response = self.client.delete("/challenge/", {})
        self.assertEqual(response.status_code, 405)        
