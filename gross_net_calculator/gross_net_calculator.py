from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class GrossNetCalculator:
    WAIT_TIME = 10

    def __init__(self, config_loader):
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")  # Run Firefox in headless mode
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(3)
        self.config = config_loader()

    def fetch_net_wages_for_all_cantons(self, gross, age, church_member, status, children):
        # Load cantons from config and remove the "All" option
        cantons = [
            canton for canton in self.config["canton"] if canton not in ["All", "Commuters"]
        ]

        # Calculate salary for commuters
        net_salary = self.calculate_net_salary(
            gross, age, church_member, status, children, "Commuters"
        )
        # The action will take us to second page https://www.lohncomputer.ch/en/your-result/
        results = {"Commuters": net_salary}
        for canton in cantons:
            # Select next canton
            self._select_dropdown_option("canton_chosen", canton)
            print(f"Fetching net salary for {canton}, please wait...")
            # Calculate and retrieve net salary
            self.driver.find_element(By.CLASS_NAME, "btn-submit-calculator").click()
            net_wage = WebDriverWait(self.driver, self.WAIT_TIME).until(
                expected_conditions.visibility_of_element_located((By.ID, "net"))
            )
            results[canton] = net_wage.text
            self.driver.implicitly_wait(1)

        return results

    def calculate_net_salary(self, gross, age, church_member, status, children, canton):
        user_msg = f"for canton: {canton}"
        if canton.lower() == "commuters":
            user_msg = "for commuters"
        print(f"Fetching net salary {user_msg}, please wait...")
        try:
            self.driver.get("https://www.lohncomputer.ch/en/calculator")

            # Gross monthly wage
            gross_box = self.driver.find_element(By.ID, "gross")
            gross_box.send_keys(str(gross))

            # Age
            age_box = self.driver.find_element(By.ID, "age")
            age_box.send_keys(str(age))

            # Church member
            checkbox = self.driver.find_element(By.ID, "church")
            is_church_member = church_member.lower() == "yes"
            if (is_church_member and checkbox.is_selected()) or (
                not is_church_member and not checkbox.is_selected()
            ):
                checkbox.click()

            # Status
            self._select_dropdown_option("marital_chosen", status)

            # Children
            self._select_dropdown_option("children_chosen", children)

            # Canton
            self._select_dropdown_option("canton_chosen", canton)

            # Calculate and retrieve net salary
            self.driver.find_element(By.CLASS_NAME, "btn-submit-calculator").click()
            net_wage = WebDriverWait(self.driver, self.WAIT_TIME).until(
                expected_conditions.visibility_of_element_located((By.ID, "net"))
            )
            return net_wage.text

        except TimeoutException:
            print(f"Failed to fetch net salary {user_msg}. The operation timed out.")
            return None

    def _select_dropdown_option(self, dropdown_id, option_text):
        dropdown = WebDriverWait(self.driver, self.WAIT_TIME).until(
            expected_conditions.element_to_be_clickable((By.ID, dropdown_id))
        )
        dropdown.click()
        option = WebDriverWait(self.driver, self.WAIT_TIME).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, f"//li[text()='{option_text}']")
            )
        )
        option.click()

    def close(self):
        self.driver.quit()
