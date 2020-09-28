from selenium import webdriver
import random
import platform


def f_open_browser(driver=None, proxy=None):
	try:
		driver.close()
		driver.quit()
	except:
		pass
	finally:
		options = webdriver.ChromeOptions()
		userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' if platform.system() == "Windows" else "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
		options.add_argument('user-agent={}'.format(userAgent))	
		options.add_argument("start-maximized")
		options.add_argument("--user-data-dir=browser_cache")
		options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
		options.add_experimental_option('useAutomationExtension', False)
		diretorio = './chromedriver.exe' if platform.system() == "Windows" else "./chromedriver"
		driver = webdriver.Chrome(options=options, executable_path=r'{}'.format(diretorio))
		return driver

def f_close_browser(driver=None):
	try:
		driver.close()
		driver.quit()
		driver = None
		return driver
	except:
		pass