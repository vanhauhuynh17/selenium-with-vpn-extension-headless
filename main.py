from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
MY_IP = "14.161.5.81"

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(
        service=service, options=chrome_options)
    
class AutomateChromeVpnExtension:
    
    def setUp(self):
        root_folder = os.getcwd()
        vpn_path = os.path.join(root_folder,"touch.crx")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_extension(vpn_path)
        chrome_options.add_argument("--headless=new")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.quit()

    def test_check_ip_has_changed(self):
        time.sleep(2)
        extension_protocol = "chrome-extension"
        extension_id = "bihmplhobchoageeokmgbdihknkjbknd"
        index_page = f"{extension_protocol}://{extension_id}/panel/index.html"
        self.driver.get(index_page)

        # Switch to the extension's panel window
        self.driver.switch_to.window(list(self.driver.window_handles)[0])
        self.driver.find_element(By.ID,"ConnectionButton").click()
        time.sleep(5)
        self.driver.get("https://nordvpn.com/what-is-my-ip/")
        # Switch back to the main window
        self.driver.switch_to.window(list(self.driver.window_handles)[0])
        # Find ip address of =============
        ip_address = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/header/div/div/div[1]/h1[2]").text
        print("ip after changed: ", ip_address)
        assert ip_address != MY_IP
      

if __name__ == "__main__":
    print("automate chrome")
    test = AutomateChromeVpnExtension()
    test.setUp()
    test.test_check_ip_has_changed()
    test.tearDown()  
# END: VPN 







