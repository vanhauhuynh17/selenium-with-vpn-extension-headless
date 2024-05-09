# Selenium with VPN: A powerful worker to scrape data in website with extension VPN in chrome

## 1. What is selenium-selenium-with-vpn-extension-headless?
- pricing-worker is a stock crawler written by Python.
- It is designed with the hope to crawl main information including:
   + Crawl data with selenium
   + Testing automation
   + Bypass authen if the website block ip
    
## 2. Quick start
Note: there is not too much difference between `python` and `python3` in our repo because we can use both to successfully run our app.

### Folder structure:
This repo is followed by a structure: https://github.com/yngvem/python-project-structure




### 2.1. How to run the app
Step 1. Install virtual env ([Ref](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/))

    python3 -m pip install --user virtualenv

Step 2. Create a virtual env and activate it ([Ref](https://docs.python.org/3/library/venv.html))

    python3 -m venv env
    source env/bin/activate

Step 3. Install python packages from the package requirement file

    make install



Step 5. Run the main app

    make run
Step 6. Check ouput:
Example: ip_address:  92.119.179.10

## 3. Options:


    MY_IP: my ip where you find in https://whatismyipaddress.com/
    HEADLESS: false open ui, if true if you want to run head to deploy to server
