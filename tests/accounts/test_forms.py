from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from YouTravel.accounts.forms import LoginForm, RegisterForm, ProfileForm

UserModel = get_user_model()


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.object.create_user(email='miro_lp@abv.bg', password='12345678')

    def test_login_form__when_is_valid(self):
        form = LoginForm(data={'email': 'miro_lp@abv.bg',
                               'password': '12345678'})
        self.assertTrue(form.is_valid())

    def test_login_form__when_is_not_valid(self):
        form = LoginForm(data={'email': 'miro1_lp@abv.bg',
                               'password': '12345678'})

        self.assertFalse(form.is_valid())
        self.assertEquals('Email/Password is incorrect', [error for field in form for error in field.errors][0])

    def test_register_form__when_is_valid(self):
        form = RegisterForm(data={'email': 'miro1_lp@abv.bg',
                                  'password1': '1q!Q2w@W',
                                  'password2': '1q!Q2w@W', })
        self.assertTrue(form.is_valid())

    def test_register_form__when_is_user_exist(self):
        form = RegisterForm(data={'email': 'miro_lp@abv.bg',
                                  'password1': '1q!Q2w@W',
                                  'password2': '1q!Q2w@W', })
        self.assertFalse(form.is_valid())
        self.assertEquals('Travel user with this Email already exists.',
                          [error for field in form for error in field.errors][0])

    def test_register_form__when_password_is_short(self):
        form = RegisterForm(data={'email': 'miro1_lp@abv.bg',
                                  'password1': '1234B',
                                  'password2': '1234B', })

        self.assertFalse(form.is_valid())
        self.assertEquals(
            'This password is too short. It must contain at least 8 characters.',
            [error for field in form for error in field.errors][0], )

    def test_profile_form__when_is_valid(self):
        form = ProfileForm(data={'first_name': 'Pesho',
                                 })
        self.assertTrue(form.is_valid())

    def test_profile_form__when_first_name_invalid_not_capitalized(self):
        form = ProfileForm(data={'first_name': 'pesho',
                                 })

        self.assertFalse(form.is_valid())
        self.assertEquals('Title must start with capitalized letter', form.errors['__all__'][0], )
