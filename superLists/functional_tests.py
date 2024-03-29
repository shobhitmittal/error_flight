from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import os,time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):

        self.driverLocation = '/home/aditya/Desktop/Test/Softwares/chromedriver'
        os.environ['webdriver.chrome.driver'] = self.driverLocation
        self.browser = webdriver.Chrome(self.driverLocation)
        self.browser.implicitly_wait(3)
        # self.browser.get('http://localhost:8002')
    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self): #
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8001')
        # She notices the page title and header mention to-do list
        self.assertIn('To-do', self.browser.title) #
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-do', header_text)
        # She is invited to enter a to-do item straight away
        # [...rest of comments as before]
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')
        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(10)
        self.check_for_row_in_list_table('1: Buy peacock feathers')


        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail('Finish the test!')
        # She visits that URL - her to-do list is still there.

if __name__ == '__main__':
    unittest.main(warnings='ignore')