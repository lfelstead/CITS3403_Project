# 
# I NEED TO REFERENCE THIS PROPERLY!!!!!!! 
# 
#To start launch from command line.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, os, time


from app import app, db
#Import more tables as needed
from app.models import Scores, User

SQLALCHEMY_TRACK_MODIFICATIONS = False

class Tester(unittest.TestCase):
    driver = None

    def setUp(self):    
        #Creates the testing envrionment by clearing and filling the database
        #and launching a chrome session to test in.

        chrome_driver_path = "chromedriver.exe"

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # create a new Chrome session
        self.driver = webdriver.Chrome(chrome_driver_path, options=options)

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
        #Removes all modifications done during testing, and shuts the testing environment
        if self.driver:
            self.driver.close()
            #Add tables as needed
            db.session.query(Scores).delete()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()

    def test_user_exists(self):
        SQLALCHEMY_TRACK_MODIFICATIONS = False

        #A simple test to determine database is functional, and can be accessesed
        u1 = User.query.get(1)
        self.assertEqual(u1.username, "real_person")

    def test_new_user(self):
        #Tests the process of creating a new user, then signing in. 
        
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
        
        
        self.driver.refresh()    
        self.driver.find_element_by_id("login").click()
        self.driver.find_element_by_id("email").send_keys("Gary@email.com")
        self.driver.find_element_by_id("password").send_keys("pAsSwOrD")
        
        time.sleep(1)
        self.driver.implicitly_wait(20)

        
        self.driver.find_element_by_id("submit").click()
        
        self.assertEqual(self.driver.find_element_by_xpath('//li[@id="login"]').get_attribute('innerHTML'), "Logout", "Should be signed in")


        
    #TODO test if password is hashed
    #Add more tests here



if __name__ == '__main__':
    unittest.main(verbosity=2)