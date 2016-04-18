import time, re                             # time.sleep, re.split
import sys                                  # some prints
import os, platform                         # for running  os, platform specific function calls
from selenium import webdriver              # for running the driver on websites
from datetime import datetime               # for tagging log with datetime

# for logging
import logging

from xvfbwrapper import Xvfb                # for creating artificial display to run experiments
from selenium.webdriver.common.proxy import *       # for proxy settings
from selenium.webdriver.common.keys import Keys

class BrowserUnit:

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        # add logging===
        self.my_log = logging.getLogger(__name__ + ".GoogleNewsUnit")
        # ==============
        self.headless = headless
        self.visiting_sites = []
        if(headless):
            self.vdisplay = Xvfb(width=1280, height=720)
            time.sleep(2)
            self.vdisplay.start()
#           if(not self.vdisplay.start()):
#               fo = open(log_file, "a")
#               fo.write(str(datetime.now())+"||"+'error'+"||"+'Xvfb failure'+"||"+'failed to start'+"||"+str(unit_id)+"||"+str(treatment_id) + '\n')
#               fo.close()
#               sys.exit(0)
        if(proxy != None):
            sproxy = Proxy({
#                'proxyType': ProxyType.MANUAL,
#                'httpProxy': proxy,
#                'ftpProxy': proxy,
#                'sslProxy': proxy,
		'socksProxy':proxy,
                'noProxy': '' # set this value as desired
                })
        else:
            sproxy = Proxy({
                'proxyType': ProxyType.AUTODETECT
                })

        if(browser=='firefox'):
            if (platform.system()=='Darwin'):
                self.driver = webdriver.Firefox(proxy=sproxy)
            elif (platform.system()=='Linux'):
                self.driver = webdriver.Firefox(proxy=sproxy)
            elif (platform.system()=='Windows'):
                self.driver = webdriver.Firefox(proxy=sproxy)
            else:
                print "Unidentified Platform"
                sys.exit(0)
        elif(browser=='chrome'):
            print "Expecting chromedriver at path specified in core/web/browser_unit"
            if (platform.system()=='Darwin'):
                chromedriver = "../core/web/chromedriver/chromedriver_mac"
            elif (platform.system() == 'Linux'):
                chromedriver = '/home/vino/Dropbox/Python/experiments2/AdFisher_Code/core/web/chromedriver/chromedriver_linux'
                 #"../core/web/chromedriver/chromedriver_linux"

            elif (platform.system() == 'Windows'):
                print "Headless Chrome is not supported yet"
                sys.exit(0)
            else:
                print "Unidentified Platform"
                sys.exit(0)
            os.environ["webdriver.chrome.driver"] = chromedriver
            chrome_option = webdriver.ChromeOptions()
            if(proxy != None):
                if sproxy.socksProxy:
                    proxy = 'socks5://' + proxy
                    chrome_option.add_argument("--proxy-server="+proxy)
            self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_option)
        else:
            print "Unsupported Browser"
            sys.exit(0)
        self.driver.implicitly_wait(10)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.driver.set_page_load_timeout(40)
        self.accept_next_alert = True
        self.log_file = log_file
        self.unit_id = unit_id
        self.treatment_id = treatment_id

    def quit(self):
        if(self.headless):
            self.vdisplay.stop()
        self.driver.quit()

    def wait(self, seconds):
        time.sleep(seconds)

    def log(self, linetype, linename, msg):     # linetype = ['treatment', 'measurement', 'event', 'error', 'meta']
        """Maintains a log of visitations"""
        fo = open(self.log_file, "a")
        fo.write(str(datetime.now())+"||"+linetype+"||"+linename+"||"+str(msg)+"||"+str(self.unit_id)+"||"+str(self.treatment_id) + '\n')
        fo.close()

    def interpret_log_line(self, line):
        """Interprets a line of the log, and returns six components
            For lines containing meta-data, the unit_id and treatment_id is -1
        """
        chunks = re.split("\|\|", line)
        tim = chunks[0]
        linetype = chunks[1]
        linename = chunks[2]
        value = chunks[3].strip()
        if(len(chunks)>5):
            unit_id = chunks[4]
            treatment_id = chunks[5].strip()
        else:
            unit_id = -1
            treatment_id = -1
        return tim, linetype, linename, value, unit_id, treatment_id

    def wait_for_others(self):
        """Makes instance with SELF.UNIT_ID wait while others train"""
        fo = open(self.log_file, "r")
        line = fo.readline()
        tim, linetype, linename, value, unit_id, treatment_id = self.interpret_log_line(line)
        instances = int(value)
        fo.close()

        fo = open(self.log_file, "r")
        for line in fo:
            tim, linetype, linename, value, unit_id, treatment_id = self.interpret_log_line(line)
            if(linename == 'block_id start'):
                round = int(value)
#       print "round, instances: ", round, instances
        fo.close()
        clear = False
        count = 0
        while(not clear):
            time.sleep(5)
            count += 1
            if(count > 1000): # increase time_out waiting for other
                self.log('event', 'wait_for_others timeout', 'breaking out')
                break
            c = [0]*instances
            curr_round = 0
            fo = open(self.log_file, "r")
            for line in fo:
                tim, linetype, linename, value, unit_id, treatment_id = self.interpret_log_line(line)
                if(linename == 'block_id start'):
                    curr_round = int(value)
                if(round == curr_round):
                    if(value=='training-start'):
                        c[int(unit_id)-1] += 1
                    if(value=='training-end'):
                        c[int(unit_id)-1] -= 1
            fo.close()
            clear = True
#           print c
            for i in range(0, instances):
                if(c[i] == 0):
                    clear = clear and True
                else:
                    clear = False
    def visit_sites(self, file_name):
        """Visits all pages in file_name"""
        #tien: count number of sites to generate the visting time
        #num_sites = sum(1 for line in open(file_name))
        import numpy
        #visit_time_array = numpy.random.exponential(90,num_sites).tolist()
        #90 seconds = 1.5 minutes
        fo = open(file_name, "r")
        for line in fo:
            if line.startswith('#'):
                continue
            self.visiting_sites.append(line.strip())
            chunks = re.split(r"\|\|", line)
            prefix = 'http://'
            if chunks[0].startswith('http:') is False:
                site = "http://"+chunks[0].strip()
            else:
                site = chunks[0].strip()
            try:
                self.driver.set_page_load_timeout(30)
                #print("Visiting site:"+site)
                self.my_log.debug('Vising site %s', site)
                self.driver.get(site)
                #time.sleep(5)
                #tien:
                #time.sleep(visit_time_array.pop())#adding sleeping time#delete
                t = numpy.random.exponential(60)
                self.my_log.debug('time stay in this webiste is: %s',str(t%30 + 5))
                self.scrolling_in_website(t%30)

                self.log('treatment', 'visit website', site)
                            # pref = get_ad_pref(self.driver)
                            # self.log("pref"+"||"+str(treatment_id)+"||"+"@".join(pref), self.unit_id)
            except Exception as e:
                # print("EXEPTION:",e)
                self.my_log.exception("Exception when visiting website")

    def collect_sites_from_alexa(self, alexa_link, output_file="sites.txt", num_sites=5):
        """Collects sites from Alexa and stores them in file_name"""
        #change from w to a, write to append
        #fo = open(output_file, "w")
        fo = open(output_file, "a")
        fo.close()
        self.driver.get(alexa_link)
        count = 0
        while(count < num_sites):
            els = self.driver.find_elements_by_css_selector("li.site-listing div.desc-container p.desc-paragraph a")
            for el in els:
                if(count < num_sites):
                    t = el.get_attribute('innerHTML').lower()
                    fo = open(output_file, "a")
                    fo.write(t + '\n')
                    fo.close()
                    count += 1
            if(count >= num_sites):# if done, must break, not find another page
                break
            self.driver.find_element_by_css_selector("a.next").click()
    def scrolling_in_website(self, sleep_time, numberOfScrollDowns = 5, disable_scroll = False):
        '''
        -- sleep_time: resting time between scrollings
        simulate mouse scrolling in a webpage
        only scroll when that is a webpage
        '''
        if True: # to make it for debugging
            sleep_time = int(sleep_time%30) + 5
        if disable_scroll is True:
            print('no scrolling at all')
            return  None
        browser = self.driver
        if self.driver.current_url.startswith('http'):
            restime = sleep_time/5
            body = browser.find_element_by_tag_name("body")
            while numberOfScrollDowns >=0:
                body.send_keys(Keys.PAGE_DOWN)
                numberOfScrollDowns -= 1
                time.sleep(restime)
            #heigh = self.driver.execute_script('return document.body.scrollHeight')
            #for i in range(5):
            #    self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight/5)")
            #    time.sleep(restime)
        return
    def scrollDown(self,numberOfScrollDowns = 5):
        browser = self.driver
        if self.driver.current_url.startswith('http'):
            body = browser.find_element_by_tag_name("body")
            while numberOfScrollDowns >=0:
                body.send_keys(Keys.PAGE_DOWN)
                numberOfScrollDowns -= 1
                time.sleep(0.5)
        return browser
