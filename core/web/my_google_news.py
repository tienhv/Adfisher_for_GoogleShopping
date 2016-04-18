import time
import re                                                     # time.sleep, re.split
import os
import sys                                                          # some prints
from collections import defaultdict, OrderedDict
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
import numpy
# import browser_unit
import my_google_ads
import google_search

import logging

# strip html

log_train = open('train_info.txt', 'w')
log_test = open('test_info.txt', 'w')
test_info = open('test_results.txt', 'w')

from HTMLParser import HTMLParser


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class GoogleNewsUnit(my_google_ads.GoogleAdsUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        my_google_ads.GoogleAdsUnit.__init__(
            self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        self.my_log = logging.getLogger(__name__ + ".GoogleNewsUnit")        
        
        # === create a file logger
        self.file_logger = logging.getLogger('suggest_logger')
        self.file_logger.addHandler(logging.FileHandler(filename=self.file_logger.name+".log",mode='a+'))
        
        # ========================
        try:
            from color_log import RainbowLoggingHandler
            #self.my_log.addHandler(RainbowLoggingHandler(sys.stdout))
            
        except:
            self.my_log.warning("There is no colorful logging")
            
        self.suggested_part = False # False: there is not `suggested for you part`
                                    # True: otherwise, default is False

    def refreshing_suggestion_page(self):
        """Refreshing the "suggested for you" every x minutes and store results        
        """
        # todo: where to store the data after every refresh
        # when there is significant test, save the screen shot
        # ==> save screenshot every time after refresh
        # call this one only in the test phase
        
        
        return
    def check_suggested_for_you_section(self,file_to_store ='suggestion_training.txt', search_term = None):
        """Checking whether 'suggested for you' section is existed on the wepage (news)
        Return:
            -- True, if yes
            -- False, otherwise
        """
        existed = False
        try:
            sg = self.driver.find_element_by_xpath('//div[@class="section story-section section-en_us-sfy"]')
            existed = True            
            #suggestion_list = []
            #sepa = "<===>"
            #tim = str(datetime.now())
            #tables  = sg.find_element_by_xpath(".//td[@class='esc-layout-article-cell']")            
            #for td in tables:
            #    title = td.find_element_by_xpath(
            #                ".//div[@class='esc-lead-article-title-wrapper']/h2/a/span").get_attribute('innerHTML')
            #    stds = td.find_elements_by_xpath(
            #        ".//div[@class='esc-lead-article-source-wrapper']/table/tbody/tr/td")
            #    agency = stds[0].find_element_by_xpath(
            #        ".//span").get_attribute("innerHTML")
            #    ago = stds[1].find_element_by_xpath(
            #        ".//span[@class='al-attribution-timestamp']").get_attribute("innerHTML")
            #    body = td.find_element_by_xpath(
            #        ".//div[@class='esc-lead-snippet-wrapper']").get_attribute('innerHTML')
            #    heading = "Suggested For You"
            #    s = tim + sepa + search_term + sepa + heading + sepa + title \
            #            + sepa + agency + sepa + ago + sepa + body + "\n"
            #    self.my_log.debug("Sugessted:\n %s", s)
            #    suggestion_list.append(s)
            # save the suggestion part to a files, for each search? YES
            #with open(file_to_store,'a+') as f:
            #    _str = "".join(suggestion_list)
            #    f.write(_str.encode('utf8'))
        except:
            self.my_log.exception("The suggestion part is not existing")
            self.my_log.debug(existed)
        #print existed
        return existed
                
    def get_suggestedstories(self):
        """Get suggested stories from Google News
        Return:
            a list of suggested stories
        """
        
        # added: store result in list
        suggested_stories = []
        sepa = "<===>"
        sys.stdout.write(".")
        sys.stdout.flush()
        try:
            self.driver.set_page_load_timeout(60)
            url = 'https://news.google.com/news/section?cf=all&topic=sfy&ned=us'
            #self.driver.get("http://news.google.com/news/section?topic=sfy")
            self.driver.get(url)
            time.sleep(5)
            tim = str(datetime.now())
            tds = self.driver.find_elements_by_xpath(
                ".//td[@class='esc-layout-article-cell']")
            for td in tds:
                title = td.find_element_by_xpath(
                    ".//div[@class='esc-lead-article-title-wrapper']/h2/a/span").get_attribute('innerHTML')
                stds = td.find_elements_by_xpath(
                    ".//div[@class='esc-lead-article-source-wrapper']/table/tbody/tr/td")
                agency = stds[0].find_element_by_xpath(
                    ".//span").get_attribute("innerHTML")
                ago = stds[1].find_element_by_xpath(
                    ".//span[@class='al-attribution-timestamp']").get_attribute("innerHTML")
                body = td.find_element_by_xpath(
                    ".//div[@class='esc-lead-snippet-wrapper']").get_attribute('innerHTML')
                #heading = "Suggested For You"
                news = strip_tags(
                    tim + sepa + title + sepa + agency + sepa + ago + sepa + body).encode("utf8")
                #self.log('measurement', 'news', news)
                suggested_stories.append(news)
        except:
            self.my_log.exception("Exception when taking suggested stories")
        return suggested_stories    


    def get_news(self, type, reloads, delay):
        """Get news articles from Google"""
        rel = 0
        while (rel < reloads):  # number of reloads on sites to capture all ads
            time.sleep(delay)
    #       try:
            for i in range(0, 1):
                s = datetime.now()
                if(type == 'top'):
                    self.get_topstories()
                elif(type == 'all'):
                    self.get_allbutsuggested()
                elif(type == 'suggested'):
                    self.get_suggestedstories()
                else:
                    raw_input("No such site found: %s!" % site)
                e = datetime.now()
                self.log('measurement', 'loadtime', str(e - s))
    #       except:
    #           log('errorcollecting', id, LOG_FILE)
    #           pass
            rel = rel + 1


# ========================================================================
    def login_news(self, username, password, dummy=False):
        """Login in Google and open Google News"""
        try:
            self.user_name = username
            self.password = password
            print ('Enter logging function')
            google = 'http://www.google.com/ncr'
            self.driver.set_page_load_timeout(60)
            self.driver.get(google)
            if dummy:
                return
            # self.driver.maximize_window()
            self.driver.find_element_by_id("gb_70").click()
            self.driver.find_element_by_id("Email").clear()
            self.driver.find_element_by_id("Email").send_keys(username)
            self.driver.find_element_by_id("next").click()
            time.sleep(5)  # to load new page
            self.driver.find_element_by_id("Passwd").clear()
            self.driver.find_element_by_id("Passwd").send_keys(password)
            time.sleep(5)

            self.driver.find_element_by_id("signIn").click()
            self.my_log.fatal('Successfull login - %s',username)
            time.sleep(5)            
            self.driver.save_screenshot('user' + str(self.unit_id) + '/' + self.user_name + '.png')
        except:
            self.log('error', 'logging in to google', username)
            self.my_log.exception('Cannot log in Google! %s',self.user_name)
    def load_train_data(self, _file_train):
        """read and store a list of training keywords"""
        l = []
        file_train = open(_file_train)
        for row in file_train:
            line = row.strip()
            if line:
                l.append(line)
        return l
    
    def read_articles_refresh(self, __file_train, count=5, agency=None, keyword=None, category=None, time_on_site=15):
        """Get top news articles from Google News"""        
        l = self.load_train_data(__file_train)
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.refresh()
            time.sleep(4)
            self.driver.get("https://news.google.com/?edchanged=1&ned=us")
        except:
            self.my_log.exception("Error loading google/ncr %s",self.user_name)        
            self.driver.get('http://example.com')
            time.sleep(10)
            self.driver.get("https://news.google.com/?edchanged=1&ned=us")
        try:
            if not os.path.exists( str(self.user_name)):
                os.makedirs(str(self.user_name))
        except:
            self.my_log.exception('error making folder to store results %s', self.user_name)
            
        filename = str(self.user_name) + '/' + self.user_name + '.txt'
        with open(filename, 'w+') as f:
            f.write(self.user_name + ": training now\n")
        # =========
        input_id = 'gbqfq'
        for keyword in l:
            self.my_log.info('Index of keywords is:' + str(l.index(keyword)) + ":" + self.user_name)
            try:              
                
                self.my_log.info('Idling for %d second',t%90)
                pattern = keyword  # +" source:Reuters"
                time.sleep(1)  # added
                if re.match(self.driver.current_url, '.*ipv4\.google\.com.*'):
                    time.sleep(20)
                    self.my_log.fatal('Google banned the ip')
                    self.driver.save_screenshot("banned.png")
                log_train.write('Searching for news about: ' + keyword)
                self.my_log.info('Searching for news about: %s', keyword +":"+ self.user_name)
                self.driver.find_element_by_id(input_id).clear()
                self.driver.find_element_by_id(input_id).send_keys(
                    pattern)
                self.driver.find_element_by_id(input_id).submit()
                time.sleep(1)
                # =========================
                to_click = []
                #tim = str(datetime.now())
                from datetime import datetime
                tim = str(datetime.now())
                news = self.driver.find_elements_by_class_name('_cnc')
                links = []
                site = self.driver.current_url
                found = False  # stiamo cercando un link di reuters
                log_train.write(site + '***********************\n')
                if 'ipv4' in self.driver.current_url:
                    self.my_log.fatal('Google banned the ip')
                if re.match(site, '.*ipv4\.google\.com.*'):
                    time.sleep(20)
                    self.my_log.fatal('Google banned the ip')
                pos = 0
                for i in range(0, 2):
                    element = news[i].find_element_by_tag_name('a')
                    curr_link = element.get_attribute('href')
                    try:
                        if True:
                            self.my_log.info(
                                'Clicking on link ' + curr_link + ' in position ' + str(i + 1))
                            element.click()
                            time.sleep(1)
                            found = True
                            log_train.write(
                                'link ' + curr_link + ' trovato alla posizione ' + str(i + 1) + '\n')
                            self.scrolling_in_website(time_on_site)
                            time.sleep(1)
                            self.my_log.info('coming back')
                            self.driver.back()
                            self.my_log.debug('Coming back to %s', self.driver.current_url)
                            time.sleep(1)
                            # break
                    except:
                        self.my_log.exception('exception when click')
                    finally:
                        news = self.driver.find_elements_by_class_name('_cnc')
                        if len(news) < 1:
                            self.driver.get("https://news.google.com/?edchanged=1&ned=us")
                            input_id = 'gbqfq'
                            break
                self.driver.get("https://news.google.com/?edchanged=1&ned=us")
            except:
                self.my_log.exception("Exception when searching:")
                self.driver.get("https://news.google.com/?edchanged=1&ned=us")
                input_id = 'gbqfq'
            t = numpy.random.exponential(90)
            time.sleep(t%90)
        log_train.close()

    def search_articlesTest(self, __file_test,  count=5, agency=None, keyword=None, category=None, time_on_site=15):
        """Get top news articles from Google News"""
        #self.driver.set_page_load_timeout(60)
        l = []
        # file_test=open('gnews/keys_test.1.txt','r')
        file_test = open(__file_test, 'r')
        self.my_log.debug(__file_test)
        for row in file_test:
            line = row.strip()
            if line:
                l.append(line)

        # ==========
        try:
            if not os.path.exists('user' + str(self.user_name)):                    
                os.makedirs('user' + str(self.user_name))
        except:
            self.my_log.exception('error making folder to store results %s', self.user_name)
        filename = 'user' + str(self.user_name) + '/' + self.user_name + '.txt'
        with open(filename, 'a+') as f:
            f.write(self.user_name + ": testing now\n")
        # ==========
        #self.driver.get("http://www.google.com/ncr")
        time.sleep(4)
        #self.driver.get("https://news.google.com/?edchanged=1&ned=us")
        input_id = 'gbqfq'
        for keyword in l:  # test_keys:
            try:
                # time.sleep (xx minutes)
                t = numpy.random.exponential(90)
                time.sleep(t % 90)
                # create folder if not existed
                try:
                    if not os.path.exists('user' + str(self.user_name)):                    
                        os.makedirs('user' + str(self.user_name))
                except:
                    self.my_log.exception('error making folder to store results')
                filename = 'user' + str(self.user_name) + '/' + keyword + '.txt'
                ris = open(filename, 'w+')

                self.driver.get("https://news.google.com/?edchanged=1&ned=us") # go_to_home_page
                
                # == checking if suggested part
                if self.check_suggested_for_you_section():
                    self.suggested_part = True
                    with open('suggested_part_existed.txt','a+') as f:
                        f.write("Suggestion\t" + keyword + " index" + str(l.index(keyword)))
                        f.write('\n')
                # == end checking =============
                log_test.write('Serching for news about: ' + keyword + '\n')
                self.my_log.info('Serching for news about: ' + keyword)
                pattern = keyword  # +" source:Reuters"
                self.driver.find_element_by_id(input_id).clear()
                self.driver.find_element_by_id(input_id).send_keys(
                    pattern)  # this is just for one keyword
                self.driver.find_element_by_id(input_id).send_keys(Keys.ENTER)#find_element_by_id(input_id).submit()
                time.sleep(2)
                # === save png screenshot here
                try:
                    png = 'user' + str(self.user_name) + '/' + keyword + '.png'
                    self.driver.save_screenshot(png)
                except:
                    self.my_log.exception('Exception when saving png')    
                # ==== end
                
                tim = str(datetime.now())
                news = self.driver.find_elements_by_class_name('_cnc')
                links = []
                site = self.driver.current_url
                found = False  # stiamo cercando un link di reuters
                log_test.write(site + '***********************\n')
                pos = 0
                tot_reu = 0
                test_info.write(str(self.user_name) + 'starting search\n')

                for n in news:
                    element = n.find_element_by_tag_name('a')
                    curr_link = element.get_attribute('href')
                    links.append(curr_link)

                for curr_link in links:
                    pos = pos + 1
                    if re.match('.*espn.*\.com.*', curr_link):
                        found = True
                        # =========
                        self.my_log.info(
                            str(self.user_name) + '\t' + keyword + '\t' + str(pos) + '\n')
                        self.my_log.info(
                            str(self.user_name) + '\t' + keyword + '\tfound\t' + str(pos) + '\n')
                        self.my_log.info(
                            str(self.user_name) + '\tlink ' + curr_link + ' trovato alla posizione ' + str(pos) + '\n')
                        # =====================
                        log_test.write(
                            str(self.user_name) + '\t' + keyword + '\t' + str(pos) + '\n')
                        test_info.write(
                            str(self.user_name) + '\t' + keyword + '\tfound\t' + str(pos) + '\n')
                        test_info.write(
                            str(self.user_name) + '\tlink ' + curr_link + ' trovato alla posizione ' + str(pos) + '\n')

                        tot_reu = tot_reu + 1

                time.sleep(30)
                test_info.write(
                    str(self.user_name) + '\t' + keyword + '\tnumNewsReuInTest\t' + str(tot_reu) + '\n')
                log_test.write(
                    str(self.user_name) + '\t' + keyword + '\tnumNewsReuInTest\t' + str(tot_reu) + '\n')

                self.my_log.info(
                    str(self.user_name) + '\t' + keyword + '\tnumNewsReuInTest\t' + str(tot_reu) + self.user_name + '\n')
                self.my_log.info(
                    str(self.user_name) + '\t' + keyword + '\tnumNewsReuInTest\t' + str(tot_reu) + self.user_name + '\n')
                # per essere precisi dovrei estrarre anche il titolo e vedere se e' uguale alla notizia che sto cercando
                # e verificare anche la data TO FIX
                if not found:
                    test_info.write(str(self.user_name) + '\t' + keyword + '\tfound\t-1\n')
                    log_test.write(str(self.user_name) + '\t' + keyword + '\t-1\n')
                for l in links:
                    ris.write(l + '\n')
                ris.close()
            except:
                self.my_log.exception('exception:')
                self.driver.get("https://news.google.com/?edchanged=1&ned=us")
                input_id = 'gbqfq'
        log_test.close()
        test_info.close()
        return
    def read_articles_espn(self, __file_train, count=5, agency=None, keyword=None, category=None, time_on_site=15):
            """Get top news articles from Google News"""
            l = []
            file_train = open(__file_train)
            for row in file_train:
                line = row.strip()
                if line:
                    l.append(line)
                    
            try:
                self.driver.set_page_load_timeout(60)
                #self.driver.refresh()
                #time.sleep(4)
                #self.driver.get("https://news.google.com/?edchanged=1&ned=us")
            except:
                self.my_log.exception("Error loading google/ncr %s",self.user_name)        
                #self.driver.get('http://example.com') # this is test domain ICANN
                #time.sleep(10)
                #self.driver.get("https://news.google.com/?edchanged=1&ned=us")
            
            try:
                if not os.path.exists('user' + str(self.user_name)):
                    os.makedirs('user' + str(self.user_name))
            except:
                self.my_log.exception('error making folder to store results %s', self.user_name)
            filename = 'user' + str(self.user_name) + '/' + self.user_name + '.txt'
            with open(filename, 'w+') as f:
                f.write(self.user_name + ": training now\n")
            # =========
            input_id = 'gbqfq'
            for keyword in l:
                self.my_log.info('Index of keywords is:' + str(l.index(keyword)) + ":" + self.user_name)
                try:
                    t = numpy.random.exponential(90)
                    time.sleep(t%90)
                    self.driver.get("https://news.google.com/?edchanged=1&ned=us")
                    # ---------------------
                    if self.check_suggested_for_you_section():
                        from datetime import datetime
                        tim = str(datetime.now())
                        self.suggested_part = True
                        self.file_logger.critical('The suggested for you part exist!')
                        with open('suggested_part_existed.txt','a+') as f:
                            f.write(tim + "\t Suggestion\t" + keyword + " index" + str(l.index(keyword)) + '\n')
                            f.write('\n')
                            self.my_log.critical('The suggested part appears')
                            log_train.close()                    
                    # ---------------------
                    self.my_log.info('Idling for %d second',t)
                    pattern = keyword  # +" source:Reuters"
                    time.sleep(1)  # added
                    if re.match(self.driver.current_url, '.*ipv4\.google\.com.*'):
                        time.sleep(20)
                        self.my_log.fatal('Google banned the ip')
                        self.driver.save_screenshot("banned.png")                                    
                    log_train.write('Searching for news about: ' + keyword)
                    self.my_log.info('Searching for news about: %s', keyword +":"+ self.user_name)
                    self.driver.find_element_by_id(input_id).clear()
                    self.driver.find_element_by_id(input_id).send_keys(
                        pattern)
                    self.driver.find_element_by_id(input_id).submit()
                    
                    time.sleep(1)

                    from datetime import datetime
                    tim = str(datetime.now())
                    news = self.driver.find_elements_by_class_name('_cnc')
                    links = []
                    site = self.driver.current_url
                    found = False  # stiamo cercando un link di reuters
                    log_train.write(site + '***********************\n')
                    if 'ipv4' in self.driver.current_url:
                        self.my_log.fatal('Google banned the ip')
                    if re.match(site, '.*ipv4\.google\.com.*'):
                        time.sleep(20)
                        self.my_log.fatal('Google banned the ip')
                    pos = 0
                    
                    for i in range(0, len(news)):                
                        element = news[i].find_element_by_tag_name('a')
                        curr_link = element.get_attribute('href')
                        try:
                            if re.match('.*espn.*\.com.*', curr_link):
                                self.my_log.info(
                                    'Clicking on link ' + curr_link + ' in position ' + str(i + 1))
                                element.click()
                                time.sleep(1)
                                found = True
                                log_train.write(
                                    'link ' + curr_link + ' trovato alla posizione ' + str(i + 1) + '\n')
                                self.scrolling_in_website(time_on_site)
                                time.sleep(1)
                                self.my_log.info('coming back')
                                self.driver.back()
                                self.my_log.debug('Coming back to %s', self.driver.current_url)
                                time.sleep(1)
                                # break
                        except:
                            self.my_log.exception('exception when click')
                        finally:
                            news = self.driver.find_elements_by_class_name('_cnc')
                            if len(news) < 1:
                                self.driver.get("https://news.google.com/?edchanged=1&ned=us")
                                input_id = 'gbqfq'
                                break
                    if not found:
                        log_train.write('non trovato\n')
                        self.my_log.info('Do not found!')
                except:
                    self.my_log.exception("Exception when searching:")
                    self.driver.get("https://news.google.com/?edchanged=1&ned=us")
                    input_id = 'gbqfq'
            log_train.close()                    
    def search_articlesTest_refresh(self,number = 500, refresh_interval = 600):
        """Go to home page Google News, then refresh to see the suggested part, 
        then store them to file (json???)
        Args:
            -- refresh_interval: interval between 2 refreshings. Default
            -- number: number of refreshing
            values is 600 second = 10 minutes
        Usage:
            -- unit.search_articlesTest_refresh(refresh_interval = 60)
        """
        LOOP = True
        iteration = 0
        tim = 0
        #news_page = "https://news.google.com/?edchanged=1&ned=us"
        news_page = "https://news.google.com/news/section?cf=all&topic=sfy&ned=us"
        self.driver.get(news_page)
        b = self.check_suggested_for_you_section()
        if b is False:
            self.my_log.fatal('There is not suggested part')
            #iteration = number + 1 # do not enter the loop
            #sys.exit()        
        # get current time
        if not os.path.exists(self.user_name):
            self.my_log.critical('Create folder to store data')
            os.makedirs(str(self.user_name))
            
        from datetime import datetime
        min_now = datetime.now().minute
        if min_now > 0:        
            min_now = 10 - min_now%10 # sleep until minutes of 10th, 20th..etc, to make all process synchronize
        #time.sleep(min_now*60)
        #if min_now % 10:
        sepa = "<===>"
        while iteration < number:
            try:
                iteration = iteration + 1
                #self.driver.get(news_page)
                time.sleep(refresh_interval)
                tim = tim + 1
                path = os.path.join(self.user_name,str(iteration)+self.user_name+'.png')
                self.driver.save_screenshot(path)
                #self.driver.refresh()
                file_name = os.path.join(self.user_name,self.user_name + ".suggested.txt")
                with open(file_name,'a+') as f2:
                    # write the suggestion part to file
                    suggested_stories = self.get_suggestedstories()
                    if suggested_stories:
                        _str = ("\n"+str(tim)+sepa).join(suggested_stories)
                        #f2.write
                        self.my_log.debug('Time\t' + str(tim) + "\n")
                        f2.write(str(tim)+sepa)
                        f2.write(_str)
                        f2.write('\n')
                    else:
                        f2.write(str(tim)+sepa+"no_suggestion\n")
                        
            except:
                # go back to home page again
                time.sleep(2)
                self.driver.get(news_page)
                self.my_log.exception("Exception when in refreshing function")
                with open(self.user_name + ".suggested.txt",'a+') as f2:
                    f2.write(str(tim)+sepa+"no_suggestion:exception\n")

def test():
    logging.basicConfig(level = logging.DEBUG)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    log = logging.getLogger(__name__)
    path = '/home/vino/Dropbox/Python/experiments2/AdFisher_Code/examples/gnews/'
    usr = '@gmail.com'
    pss = ''
    unit = GoogleNewsUnit(
        browser='firefox', log_file='delte.txt', unit_id=0,
        treatment_id=0, headless=False, proxy=None) #'127.0.0.1:3001'
    unit.login_news(usr,password=pss)
    unit.driver.get("https://news.google.com/?edchanged=1&ned=us")
    #unit.driver.get('http://whatismyipaddress.com/')
    #time.sleep(15)
    # no logging
    #unit.visit_sites(path + 'espn.1.txt')
    #unit.read_articles(path + 'keys_train.1.txt', count=3, agency='Reuters',
    #                   keyword=None, category=None, time_on_site=20)
    #unit.search_articlesTest(
    #    path + 'keys_test.1.txt', count=3, agency='Reuters', keyword=None, category=None, time_on_site=20)
    #unit.check_suggested_for_you_section(
    #                                    file_to_store='suggestion_training.txt', 
    #                                    search_term=None)
    #print unit.get_suggestedstories()
    unit.search_articlesTest_refresh(number=2, refresh_interval=3)
    unit.quit()


TEST = False
if TEST:
    test()
