import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Page Object Model (POM) classes
class LoginPage:
    def _init_(self, driver):
        self.driver = driver
        self.username_textbox = (By.NAME, "username")
        self.password_textbox = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.forgot_password_link = (By.LINK_TEXT, "Forgot your password?")

    def enter_username(self, username):
        self.driver.find_element(*self.username_textbox).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_textbox).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()

    def click_forgot_password_link(self):
        self.driver.find_element(*self.forgot_password_link).click()

class AdminPage:
    def _init_(self, driver):
        self.driver = driver
        self.page_title = (By.XPATH, "//h1[contains(text(), 'OrangeHRM')]")
        self.admin_menu_items = (By.XPATH, "//ul[@class='oxd-main-menu']/li")

    def validate_page_title(self, expected_title):
        actual_title = self.driver.find_element(*self.page_title).text
        assert actual_title == expected_title, f"Expected title: {expected_title}, Actual title: {actual_title}"

    def validate_admin_menu_items(self, expected_items):
        menu_items = self.driver.find_elements(*self.admin_menu_items)
        actual_items = [item.text.strip() for item in menu_items]
        assert set(expected_items) == set(actual_items), f"Expected menu items: {expected_items}, Actual menu items: {actual_items}"

# Test data for Data Driven Testing
test_data = [
    ("valid_user", "valid_password"),
    ("invalid_user", "valid_password"),
    ("valid_user", "invalid_password"),
    ("invalid_user", "invalid_password"),
]

@pytest.fixture(scope="class")
def setup(request):
    global driver
    driver = webdriver.Chrome()  # Adjust driver path if needed
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("setup")
class TestLogin:

    def test_forgot_password_link(self):
        login_page = LoginPage(self.driver)
        login_page.click_forgot_password_link()
        wait = WebDriverWait(self.driver, 10)
        username_box = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        assert username_box.is_displayed(), "Username textbox is not visible"
        username_box.send_keys("test_user")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Reset password link sent successfully')]")))
        assert success_message.is_displayed(), "Reset password success message not displayed"

    @pytest.mark.parametrize("username,password", test_data)
    def test_login(self, username, password):
        login_page = LoginPage(self.driver)
        login_page.enter_username(username)
        login_page.e
