from django.contrib.auth import get_user_model
from django.test import TestCase, Client



UserModel = get_user_model()


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.object.create_user(email='miro_lp@abv.bg', password='12345678')



