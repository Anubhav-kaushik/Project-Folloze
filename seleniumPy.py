from lib2to3.pgen2 import driver
from selenium import webdriver


driver = webdriver.Firefox(executable_path=r'F:\ProjectFolloze\follozeEnv\driver\geckodriver.exe')
driver.get("https://www.google.com")

