from output_logs import app
import unittest

class FlaskTestCase(unittest.TestCase):

    def check_status(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        print('Application status code: ', statuscode)
        self.assertEqual(statuscode, 200)
    
if __name__ == '__main__':
    unittest.main()