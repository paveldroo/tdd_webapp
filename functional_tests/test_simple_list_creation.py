from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        # Once upon a time User has heard about cool To-Do App. He goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # He noticed the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting ger to add another item. He enters "Use peacock feathers" to make a fly"
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Ivan starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # He notices that his list has a unique URL
        ivan_list_url = self.browser.current_url
        self.assertRegex(ivan_list_url, '/lists/.+')

        # Now a new user, Maria, comes aling to the site

        # We use a new browser session to make sure that no information of Ivan's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Maria visits the home page. There is no sign of Ivan's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Maria starts a new list by entering a new item. He is less interesting than Ivan's...
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Maria gets her own unique URL
        maria_list_url = self.browser.current_url
        self.assertRegex(maria_list_url, '/lists/.+')
        self.assertNotEqual(ivan_list_url, maria_list_url)

        # Again, there is no trace of Ivan's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
