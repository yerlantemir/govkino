
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from authentication.models import User


# Create your tests here.

class UserAuthTest(APITestCase):

    def setUp(self):
        self.client = self._get_client_with_user("yerlantemir", with_token=True)
        self.user = self.client.user

    def test_sms_sign_in(self):
        client = self._get_client_with_user("yerlan2")
        res_sign_in = client.post(reverse('sms-sign-in'), data={"username": client.user.username})
        self.assertEqual(res_sign_in.status_code, status.HTTP_200_OK)
        self.assertNotEqual('', res_sign_in.data['code'])

        res_sign_in2 = client.post(reverse('sms-sign-in'), data={"username": "not-existing-username"})
        self.assertEqual(res_sign_in2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_verification(self):
        client = self._get_client_with_user("yerlan2")
        res_sign_in = client.post(reverse('sms-sign-in'), data={"username": client.user.username})

        res_sign_in_verify_ok = client.post(reverse('sms-sign-in-verify'), data={"code": res_sign_in.data['code']})
        self.assertEqual(res_sign_in_verify_ok.status_code, status.HTTP_201_CREATED)

        res_sign_in_verify_not_ok = client.post(reverse('sms-sign-in-verify'), data={"code": 'not-existing-code'})
        self.assertEqual(res_sign_in_verify_not_ok.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_sign_in(self):
        client = self._get_client_with_user("yerlan2")
        res_sign_in_ok = client.post(reverse('password-sign-in'), data={'username': "yerlan2", 'password': "12345"})
        self.assertEqual(res_sign_in_ok.status_code, status.HTTP_200_OK)

        res_sign_in_not_ok = client.post(reverse('password-sign-in'), data={'username': 'yerlan2',
                                                                            'password': 'non-existing-password'})
        self.assertEqual(res_sign_in_not_ok.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_view(self):
        client = APIClient()

        res_of_sign_up = client.post(reverse('sign-up'), data={'username': 'yerlan2',
                                                               'password': '123',
                                                               'phone_number': '+77762447712'})
        self.assertEqual(res_of_sign_up.status_code, status.HTTP_201_CREATED)

        self.assertNotEqual('', res_of_sign_up.data['code'])

        res_of_sign_up2 = client.post(reverse('sign-up'), data={'username': 'yerlan2',
                                                                'password': '123',
                                                                'phone_number': '+2277762447712'})
        self.assertEqual(res_of_sign_up2.status_code, status.HTTP_400_BAD_REQUEST)

        res_of_sign_up3 = client.post(reverse('sign-up'), data={'username': 'yerlantemir',
                                                                'password': '123',
                                                                'phone_number': '+77762447712'})
        self.assertEqual(res_of_sign_up3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_verify(self):
        client = APIClient()

        res_of_sign_up = client.post(reverse('sign-up'), data={'username': 'yerlan2',
                                                               'password': '123',
                                                               'phone_number': '+77762447710'})
        len_before = len(User.objects.all())
        res_of_sign_up_verification = client.post(reverse('sign-up-verify'), data={'code': res_of_sign_up.data['code']})
        len_after = len(User.objects.all())

        self.assertEqual(res_of_sign_up_verification.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len_after - len_before, 1)

    def _get_client_with_user(self, username, with_token=False):
        user = User(**{"username": username, "phone_number": "+77772537792", "password": "12345"})
        user.save()

        client = APIClient()

        if with_token:
            token = Token.objects.create(user=user)
            client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        client.user = user

        return client
