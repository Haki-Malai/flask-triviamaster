from tests.base_test_case import BaseTestCase


class TestMainRoute(BaseTestCase):

    def test_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>%b</title>' % self.app.config['TITLE'].encode(),
                      response.data)
        self.assertIn(b'<h5 class="mt-3">Or choose a category below to get started:</h5>',
                      response.data)