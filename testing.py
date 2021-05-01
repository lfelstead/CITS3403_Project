# 
# I NEED TO REFERENCE THIS PROPERLY!!!!!!! 
# 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, os, time


from app import app, db
#Import more tables as needed
from app.models import Scores, User





class Tester(unittest.TestCase):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    driver = None

    def setUp(self):    
        chrome_driver_path = "chromedriver.exe"

        # create a new Chrome session
        self.driver = webdriver.Chrome(chrome_driver_path)

        if not self.driver:
            self.skipTest("No Web Browser Found")

        else:
            db.init_app(app)
            db.create_all()

            #Add new database modifications here

            user1 = User(username = "real_person", email = "email@provider.com", password = "hunter2")
            db.session.add(user1)
            db.session.commit()
            self.driver.implicitly_wait(30)
            self.driver.maximize_window()

            # Navigate to the application home page
            self.driver.get("http://127.0.0.1:5000/")


    def tearDown(self):
        if self.driver:
            self.driver.close()
            #Add tables as needed
            db.session.query(Scores).delete()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()

    def test_sanity(self):
        self.assertEqual(1, 1)

    def test_user_exists(self):
        u1 = User.query.get(1)
        self.assertEqual(u1.username, "real_person")

    def test_new_user(self):
        self.driver.get("http://127.0.0.1:5000/register")
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id("username").send_keys("Gary")
        self.driver.find_element_by_id("email").send_keys("Gary@email.com")
        self.driver.find_element_by_id("password").send_keys("pAsSwOrD")
        self.driver.find_element_by_id("confirm").send_keys("pAsSwOrD")


        time.sleep(1)
        self.driver.implicitly_wait(20)

        self.driver.find_element_by_id("submit").click()

        time.sleep(1)
        self.driver.implicitly_wait(20)
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)