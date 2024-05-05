import time

import undetected_chromedriver as uc

import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By


class CoinSniperVoter():
    def __init__(self):
        self.headless = False
        self.driver: WebDriver
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        self.login_details = "EMAIL:PASSWORD".split(":")
        self.selectors = {
            "email": "input[name='email']",
            "password": "input[name='password']",
            "login_btn": "input[type='submit']",
            "accept_cookies": ".modal-card button"
        }
        
    def init_webdriver(self):
        options = uc.ChromeOptions()

        options.add_argument("--log-level=4")
        options.add_argument(f'--profile-directory=defualt')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--disable-notifications")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-zygote')
        options.add_argument(f"user-agent={self.user_agent}")

        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1,
            "excludeSwitches": ["enable-automation", "disable-popup-blocking"],
            'useAutomationExtension': False,
        })

        capabilities = DesiredCapabilities.CHROME
        capabilities['goog:loggingPrefs'] = {"performance": "ALL"}

        self.driver = uc.Chrome(options=options, desired_capabilities=capabilities, headless=self.headless)

        self.driver.maximize_window()
        self.driver.set_page_load_timeout(5*60)  # 5 minutes


    def login(self) -> bool:
        self.driver.get("https://coinsniper.net/login")
        
        login_container = WebDriverWait(self.driver, timeout=120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors["email"]))
        )
        
        # time.sleep(60000)
        self.driver.find_element(By.CSS_SELECTOR, self.selectors["accept_cookies"]).click()
        
        self.driver.find_element(By.CSS_SELECTOR, self.selectors["email"]).send_keys(self.login_details[0])
        self.driver.find_element(By.CSS_SELECTOR, self.selectors["password"]).send_keys(self.login_details[1])

        self.driver.find_element(By.CSS_SELECTOR, self.selectors["login_btn"]).click()

        self.sleep_for_x_mins(10/60)

    def sleep_for_x_mins(self, mins: int) -> bool:
        time.sleep(mins*60)

    def run(self):
        self.init_webdriver()
        
        try:
            self.login()
            self.driver.go

        except Exception as e:
            print(f"An error occured: {e}")
            self.driver.quit()
            
        self.driver.quit()


if __name__ == "__main__":
    voter = CoinSniperVoter()
    voter.run()