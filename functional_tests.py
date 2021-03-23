import unittest

from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Once upon a time User has heard about cool To-Do App. He goes
        # to check out its homepage
        self.browser.get('http://127.0.0.1:8000')

        # He noticed the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # He is invited to enter a to-do item straight away

        # He types "Buy peacock feathers" into a text box

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting ger to add another item. He enters "Use peacock feathers" to make a fly"

        # The page updates again, and now shows both items on his list

        # User wonders whether the site will remember his list.Then he sees that
        # the site has generated a unique URL for him.

        # User visites that URL - his to-do list is still there

        # Satisfied, he goes back to sleep


if __name__ == '__main__':
    unittest.main()
