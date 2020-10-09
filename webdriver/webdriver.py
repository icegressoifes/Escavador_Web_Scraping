from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import random
import platform
import logging
import logging.config
import traceback

# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
msg_error = "\nErro: "+__name__+".py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."


def f_open_browser(driver=None, proxy=None):
	try:
		driver.close()
		driver.quit()
	except:
		pass
	
	try:
		options = webdriver.ChromeOptions()
		userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' if platform.system() == "Windows" else "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
		options.add_argument('user-agent={}'.format(userAgent))	
		options.add_argument("start-maximized")
		options.add_argument('window-size=1900,1080')    
		# options.add_argument('--disable-gpu')
		# options.add_argument('--disable-extensions')
		# options.add_argument("--disable-dev-shm-usage")
		options.add_argument('--no-sandbox')
		options.add_argument("--user-data-dir=browser_cache")
		options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
		options.add_experimental_option('useAutomationExtension', False)
		prefs = {"profile.password_manager_enabled": True, "credentials_enable_service": True}
		options.add_experimental_option("prefs", prefs)  
		# driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME, options=options)
		diretorio = './chromedriver.exe' if platform.system() == "Windows" else "./chromedriver"
		driver = webdriver.Chrome(options=options, executable_path=r'{}'.format(diretorio))
		return driver
	except:
		
		if "Message: 'chromedriver' executable needs to be in PATH" in str(traceback.format_exc()):
   			print(msg_error.format("função f_open_browser", "ChromeDriver não encontrado"))		
		elif "This version of ChromeDriver only supports Chrome version" in str(traceback.format_exc()):
   			print(msg_error.format("função f_open_browser", "Versão do ChromeDriver está desatualizada"))
		else:
			print(msg_error.format("função f_open_browser", "Não conseguiu abrir o navegador"))
		logger.error( traceback.format_exc() )
		raise
		

def f_close_browser(driver=None):
	try:
		driver.close()
		driver.quit()
		driver = None
		return driver
	except:
		pass
