import os
import logging
import logging.config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SocialBot():
    def __init__(self, driver=None):
        self.logger = get_logger()
        if driver is None:
            self.logger.debug("Creating Chrome Driver With Options...")
            chrome_options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_experimental_option("prefs", { \
                "profile.default_content_setting_values.notifications": 2 # 1:allow, 2:block
            })
            driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
            self.logger.debug("Chrome Driver Created.")
        self.browser = driver
        self.wait = WebDriverWait(self.browser, 10)
        super().__init__()

    def _login(self, url, username, password, element_user, element_pass, element_login):
        self.logger.info(f"Navigating to - {url}")
        self.browser.get(url)
        self.logger.debug(f"Locating elements: 1) {element_user}, 2) {element_pass}, 3) {element_login}")
        try:
            input_username = self.browser.find_element_by_id(element_user)
            input_password = self.browser.find_element_by_id(element_pass)
            form = self.browser.find_element_by_name(element_login)
        except NoSuchElementException as e:
            self.logger.critical(str(e))
            raise(NoSuchElementException)
        self.logger.debug("Sending Keys...")
        input_username.send_keys(username)
        input_password.send_keys(password)
        self.logger.debug("Keys Sent. Submit.")
        form.click()

    def navigate_home(self):
        self.browser.get(self.base_url)
    
    def navigate_to_page(self, url):
        self.wait.until(EC.url_changes(url))
        self.browser.get(url)
    
    def quit(self):
        self.browser.quit()

class Facebook(SocialBot):
    base_url = "https://facebook.com/"
    mobile_url = "https://m.facebook.com/"

    def login(self, username, password):
        self.logger.info("Preparing login...")
        self._login(self.base_url, username, password,
        "email", "pass", "login")

    def post_to_group(self, group_id, content):
        self.logger.info(f"Navigating to - {self.mobile_url+group_id}")
        self.navigate_to_page(self.mobile_url + group_id)

        self.logger.info("Submitting Post...")
        self.logger.debug(f"Retrieving 'what's on your mind? (woym)' element")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div[3]/div/div[1]/div[2]/div')))
        whats_on_your_mind = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div/div[3]/div/div[1]/div[2]/div')
        post_input = whats_on_your_mind.find_element_by_xpath('..')
        self.logger.debug("Found woym element. Clicking...")
        post_input.click()

        self.logger.debug(f"Retrieving Post Text Area element")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/div/div/div[5]/div[3]/form/div[3]/div[3]/textarea')))
        post_text_area = self.browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div/div/div[5]/div[3]/form/div[3]/div[3]/textarea')

        self.logger.debug("Constructing Post...")

        ### Construct message to post ###
        #################################
        post_text_area.send_keys(content["title"])
        post_text_area.send_keys(Keys.ENTER)
        post_text_area.send_keys(content["hashtag"])
        post_text_area.send_keys(Keys.ENTER)
        post_text_area.send_keys(content["url"])

        self.logger.debug("Retrieving Post Button element")
        post_btn = self.browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div/div/div[5]/div[3]/div/div/button')
        post_btn.click()

        self.logger.debug("Post submitted. Waiting for Facebook feedback.")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Your post is now published.')]")))

def execute(content):
    email = os.environ.get('BOT_USERNAME')
    password = os.environ.get('BOT_PASSWORD')
    group_id = os.environ.get('BOT_GROUP_ID')

    logger = get_logger()
    logger.info("Executing SocialBot...")

    try:
        bot = Facebook()
        bot.login(email, password)
        bot.post_to_group(group_id, content)
    except NoSuchElementException as nsee:
        logger.critical("NoSuchElementException was thrown. " + str(nsee))
    finally:
        bot.quit()
        logger.info("SocialBot Finished.")

def get_logger():
    logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
    logging.config.fileConfig(logging_conf_path)
    return logging.getLogger("FBPostLogger")