from rest_framework.test import APITestCase

# Create your tests here.

class UserTest(APITestCase):

    def test_user_register(self):

        data = {
            "name" : "ben",
            "password": "parker123"
        }
        res = self.client.post('/register', data)

        self.assertEqual(res.json()['message'], "User registered successfully")


    def test_user_register_params(self):

        data = {
            "name" : "ben",
            "password": "parker"
        }
        res = self.client.post('/register', data)

        self.assertEqual(res.json()['message'], "password length should be 8 or more")


class AuthTokenTest(APITestCase):

    def test_token(self):

        res = self.client.get('/authorize', headers={
            'Authorization': ''
        })
        self.assertEqual(res.json()['error'], 'Token is missing')

    def test_invalid_token(self):

        res = self.client.get('/authorize', headers={
            'Authorization': 'jsfdghjklrjk'
        })
        self.assertEqual(res.json()['error'], 'Invalid token')

    def test_valid_token(self):
        # for this test to pass change token in authorization header
        res = self.client.get('/authorize', headers={
            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE3MDU2MDI4Nzd9.iVsptk4U_Xu95kg8A12eJAuqz9UzUG3v20exgbjtrf8'
        })
        self.assertEqual(res.json()['message'], 'Api authorized with token successfully!')


class WeatherApiTest(APITestCase):

    def test_api_params(self):

        res = self.client.get('/weather?&latitude=&longitude=13.41&days=10')
        self.assertEqual(res.json()['message'], "latitude required")


    def test_api_response(self):

        res = self.client.get('/weather?latitude=52.23&longitude=13.41&days=10')

        data = res.json()
        l = [s for s in data.keys()]

        self.assertEqual(l, ['hourlyTemperature', 'precipitation', 'cloudCover'])

