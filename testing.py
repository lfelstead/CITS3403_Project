# 
# I NEED TO REFERENCE THIS PROPERLY!!!!!!! 
# 
#To start launch from command line.
from app import bcrypt
from selenium import common, webdriver
from selenium.webdriver.common.keys import Keys
import unittest, os, time


from app import app, db
#Import more tables as needed
from app.models import Scores, User


def encrypt(password):
    #simulates the encryption done by the routes 
    return(bcrypt.generate_password_hash(password).decode('utf-8'))

class Tester(unittest.TestCase):
    driver = None

    # db.session.query(Scores).delete()
    # db.session.query(User).delete()
    # db.session.commit()
    # db.session.remove()

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
            user1 = User(username = "real_person", email = "email@provider.com", password = encrypt("hunter2"))
            user2 = User(username = "user_101", email = "user_@provider.com", password = encrypt("password1"))
            user3 = User(username = "best_user", email = "_bestemail@provider.com", password = encrypt("qwerty"))
            user4 = User(username = "human", email = "humanname@provider.com", password = encrypt("123456"))
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.add(user4)

            db.session.commit()

            scores1 = Scores(questionid = 1, correct = True, attempt = 0 , userid = user3.id)
            scores2 = Scores(questionid = 2, correct = False, attempt = 0 , userid = user3.id)
            scores3 = Scores(questionid = 3, correct = True, attempt = 0 , userid = user3.id)
            scores4 = Scores(questionid = 4, correct = True, attempt = 0 , userid = user3.id)
            scores5 = Scores(questionid = 5, correct = False, attempt = 0 , userid = user3.id)

            scores6 = Scores(questionid = 6, correct = True, attempt = 3 , userid = user1.id)
            scores7 = Scores(questionid = 2, correct = False, attempt = 0 , userid = user2.id)
            scores8 = Scores(questionid = 3, correct = True, attempt = 1 , userid = user2.id)
            scores9 = Scores(questionid = 4, correct = True, attempt = 0 , userid = user4.id)
            scores10 = Scores(questionid = 4, correct = False, attempt = 1 , userid = user4.id)

            db.session.add(scores1)
            db.session.add(scores2)
            db.session.add(scores3)
            db.session.add(scores4)
            db.session.add(scores5)
            db.session.add(scores6)
            db.session.add(scores7)
            db.session.add(scores8)
            db.session.add(scores9)
            db.session.add(scores10)

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
        #A simple test to determine database is functional, and can be accessesed
        u1 = User.query.get(1)
        self.assertEqual(u1.username, "real_person")

    def test_email(self):
        u1= User.query.get(1)
        self.assertEqual(u1.email, "email@provider.com")

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
        self.driver.find_element_by_id("email").send_keys("Gary@email.com")
        self.driver.find_element_by_id("password").send_keys("pAsSwOrD")
        
        time.sleep(1)
        self.driver.implicitly_wait(20)

        
        self.driver.find_element_by_id("submit").click()
        
        try: 
            self.driver.find_element_by_xpath('//a[@href="/account/Gary"]')

        except common.exceptions.NoSuchElementException:
            self.fail("NoSuchElementException therefore not signed in")
        
    def test_score_exists(self):
        u3 = User.query.get(3)      
        self.assertEqual(str(Scores.query.filter_by(userid=u3.id).first()), "Scores('1', 'True', '0')")

if __name__ == '__main__':
    unittest.main(verbosity=2)