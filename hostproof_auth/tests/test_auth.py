from django.test import TestCase
from django.db import IntegrityError

from hostproof_auth.models import *
from hostproof_auth.auth import ModelBackend

class ModelBackendTest(TestCase):
    def setUp(self):
        self.modelBackend = ModelBackend()
        self.user = User.objects.create_user(username="john",
                        email="john.smith@domain.com",
                        challenge="randomstring",
                        encrypted_challenge="encryptedrandomstring")

    def test_authenticate_valid_user(self):
        user = self.modelBackend.authenticate("john", "randomstring")
        self.assertIsNotNone(user)

    def test_authenticate_invalid_user(self):
        user = self.modelBackend.authenticate("non_existing", "randomstring")
        self.assertIsNone(user)

    def test_authenticate_invalid_challenge(self):
        user = self.modelBackend.authenticate("john", "invalid")
        self.assertIsNone(user)

    def test_get_user_valid_user(self):
        user = self.modelBackend.get_user(self.user.pk)
        self.assertEquals(user, self.user)

    def test_get_user_invalid_user(self):
        user = self.modelBackend.get_user(-1)
        self.assertIsNone(user)
