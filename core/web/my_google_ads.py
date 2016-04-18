# pylint: disable=line-too-long, unnecessary-parens
# This line of text does nothing
import traceback
import logging
import json
import numpy
import collections
import time
import re
import os  # time.sleep, re.split, os,
import sys
from selenium import webdriver  # for running the driver on websites
from datetime import datetime  # for tagging log with datetime
from selenium.webdriver.common.keys import Keys  # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains  # to move mouse over
from selenium.common.exceptions import TimeoutException
import google_search
import price_utilities

# Google ad settings page class declarations


# TIEN
MEAN_VISIT = 30 # mean of visiting time for one website
# the list of constant for json key
USER_NAME = 'user_name'
SERIAL = 'serial'
AVERAGE_PRICE = 'average_price'
SEARCHING_TERM = 'searching_term'
PRICE_DATA = 'price_data'
CLICKED_LINKS = 'clicked_links'
CLICKED_LINKS_GDN = 'clicked_links_gnd'
#
LOG_SEPARATE_LINE = "ENDLING__LINE"
input_shop_id = 'gbqfq'
GOOGLE_SHOP_URL = 'http://shopping.google.com/?&hl=en'
DEFAULT_CONDITION_CLICK_PRICE = 3  # click on the most expensive link
PRICE_FILE = '_price.txt'

GENDER_DIV = "qJ oZ"
AGE_DIV = "qJ cZ"
LANGUAGES_DIV = "qJ uZ"
INTERESTS_DIV = "qJ h0"

OPTIN_DIV = "to Uj kZ"
OPTOUT_DIV = "UZ Uj BL"
EDIT_DIV = "to Uj c-eb-qf c-eb-Jh"
RADIO_DIV = "a-z rJ c0"
SUBMIT_DIV = "c-ba-aa a-b a-b-E ey"
ATTR_SPAN = "Fn"

EDIT_DIV_SIGNIN = "Uj Ks c-eb-qf c-eb-Jh"

LANG_DROPDOWN = "c-ba-aa c-g-f-b a-ra xx"
LANG_DIV = "c-l"

PREF_INPUT = "j0 a-na nU"
PREF_TR = "mU tx f0"
PREF_TD = "qA g0"
CROSS_TD = "rA"
PREF_OK_DIV = "c-ba-aa a-b a-b-E rT yL"

SIGNIN_A = "gb_70"
GOOGLE_SEARCH_URL = "https://www.google.com/ncr"
# strip html
XPATH_RESULT = "//div[@class='rc']/h3[@class='r']/a"
GENDER_DIV = "EA yP"
INPUT_ID = "lst-ib"
LI_CLASS = "g"

SIGNIN_A = "gb_70"

GOOGLE_SEARCH_URL = "https://www.google.com/ncr"



from HTMLParser import HTMLParser


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

class ConcatJSONDecoder(json.JSONDecoder):
    """from http://stackoverflow.com/questions/8730119/retrieving-json-objects-from-a-text-file-using-python.
    ----This class used to read json list
    ----{}{}{}
    --- How to use:
    print json.loads('{}', cls=ConcatJSONDecoder)
    print json.load(open('file'), cls=ConcatJSONDecoder)
    print json.loads('{}{} {', cls=ConcatJSONDecoder)
    """
    FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
    WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            objs.append(obj)
        return objs

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def last_line(file_):
    """
    file_ -- is file's name
    return the last line (after call string.strip())
    """
    with open(file_, "rb") as f:
        first = f.readline()      # Read the first line.
        f.seek(-2, 2)             # Jump to the second last byte.
        while f.read(1) != b"\n":  # Until EOL is found...
            f.seek(-2, 1)         # ...jump back the read byte plus one more.
        last = f.readline()     # Read last line.
        return last.strip()
        # print last


class GoogleAdsUnit(google_search.GoogleSearchUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        google_search.GoogleSearchUnit.__init__(
            self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        # browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id,
        # treatment_id, headless, proxy=proxy)
        self.isLogin = False
        self.user_name = "no_email"
        self.password = "no_password"
        self.personas = False
        self.visited_list = []
        self.driver.set_page_load_timeout(60)
        self.my_log = logging.getLogger('google_search.GoogleSearchUnit')

    def opt_in(self):
        pass

    def opt_out(self):
        pass

    def create_folder(self, directory):
        """create folder to store all files: html, txt"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        return

    def login_google(self, username, password, dummy_login=False):
        """Login to Google with username and password

        Args:
            username:
            password:
            dummy_login: True - non login account (aka fresh user), True - login
        """

        if dummy_login:
            self.user_name = username
            self.password = password
            return
        try:
            self.my_log.debug('Enter logging function')
            google = 'http://www.google.com/ncr'
            #self.driver.maximize_window()
            self.driver.get(self.base_url)
            self.driver.find_element_by_id("gb_70").click()
            self.driver.find_element_by_id("Email").clear()
            self.driver.find_element_by_id("Email").send_keys(username)
            self.driver.find_element_by_id("next").click()
            time.sleep(5)
            self.driver.find_element_by_id("Passwd")
            self.driver.find_element_by_id("Passwd").clear()
            self.driver.find_element_by_name('Passwd')

            self.my_log.debug('sending password')
            self.driver.find_element_by_id("Passwd").send_keys(password)
            time.sleep(3)
            self.driver.find_element_by_id("signIn").click()
            self.isLogin = True  # set login is tru   e
            self.user_name = username
            self.password = password
            #print('>>Non-Dummy',username+password)
            # self.create_folder(self.user_name)
            # create folder according to log_file_name
            self.create_folder(self.log_file[:-4])
            self.log('treatment', 'login', username)
            self.my_log.critical("Log in google successfully!")
        except Exception as e:
            self.log('error', 'logging in to google', username)
            self.my_log.critical("Log in google unsuccessfully!")
        time.sleep(3)

        #
    def save_log(self, file_name, suffix):
        #print('>save_log:' + str(self.isLogin))
        #print('>save_log:' + file_name)
        time.sleep(1)
        with open(os.path.join(self.log_file[:-4], suffix + '.txt'), 'a') as f:
            f.write(self.user_name + "|age|gender|" + "number_of_click" + "|" + "n_history" + "|" + file_name + "|" + str(datetime.now(
            )) + "\n")
        # -START-16-Dec###################
    #@classmethod
    #def load_visited_websites2(self,file_1):
    #    """Read training webiste and store in a list (without visite those sites)
    #    """
    #    visited_list = []
    #    f = open(file_1, 'rt')
    #    for line in f:
    #        if line.startswith('#'):
    #            print line
    #            continue
    #        visited_list.append(line.strip())
    #    f.close()
    #    return visited_list
    def load_visited_websites(self, file_):
        """Read training webiste and store in a list (without visite those sites)
        """
        f = open(file_, 'rt')
        for line in f:
            if line.startswith('#'):
                continue
            self.visited_list.append(line.strip())
        f.close()
        self.my_log.debug("list of visit websites:%s",self.visited_list)

    def create_new_file_name(self, email, term):  # folder, term is suffix
        """
        generate file_name for new saving file.
        email: folder_name, a@imtluca.it/...term.*.html.
        """
        import os
        i = 0
        # if self.isLogin == False:
            # email = 'nologin'
        name = email + "." + term + "." + str(i) + ".html"
        while (os.path.exists(os.path.join(self.log_file[:-4], name))):
            i = i + 1
            name = email + "." + term + "." + str(i) + ".html"
        # write to log file
        # file for
        self.my_log.debug("Name is %s",name)
        return name

    def save_html_page(self, html, email, term,saving=True):
        """
        saving html page to disk.
        """
        html_name = self.create_new_file_name(email, term)
        if saving is True:
            self.my_log.debug('Going to save %s',html_name)
            with open(os.path.join(self.log_file[:-4], html_name), 'w') as temp_file:
                print('saving thml')
                temp_file.write(html)
        return html_name
    # 18/12/2015
        # combine the training and testing_phase function into one function
    # they are nearly identical!

    def search_for_measuring_price(self, terms, price_condition=3, number_of_results_to_click=3, training=True):
        '''
        training: True if this is training, False if this is testing phase\n
        This is for testing/training phase.\n
        Step1: Search for  a keyword\n
        Step2: Save results\n
        Step22:(for training) click on n-most-expensive products\n
        Step3: Repeat for other keywords if available\n
        terms: a Python list of products\n

        price_condition: condition of the results to be clicks\n

        price_condition = 'low': for results have price below average\n
        price_condition = 'high': that of above average\n
        This one is for compatible reason: price_condition = 3 (default value): click on the top 3 most expensive results' prices.\n
        do not use/set number_of_results_to_click when price_condition is interger\n
        '''

        self.driver.set_page_load_timeout(60)
        # read serial number here
        ultima_line = ''
        ultima_line = LOG_SEPARATE_LINE + "@_@0\n"
        file_name = ''
        serial = 0
        self.my_log.debug('value of training is:'+str(training))
        if training is False:
            file_name = "testing_" + self.user_name + PRICE_FILE
            file_name = os.path.join(self.log_file[:-4], file_name)
            if os.path.isfile(file_name):
                ultima_line = last_line(file_name)
                serial = int(ultima_line.split('@_@')[1])
                ultima_line = LOG_SEPARATE_LINE + \
                    "@_@" + str(serial + 1) + "\n"
                self.my_log.debug('ultima line:'+ ultima_line)
                serial = int(ultima_line.split('@_@')[1])
            #
        for term in terms:

            self.my_log.debug(">Enter measurement function " + str(self.user_name))
            file_namep = "training_" + self.user_name + PRICE_FILE
            if training is False:
                file_namep = "testing_" + self.user_name + PRICE_FILE            
            try:
                time.sleep(2)
                self.driver.get(GOOGLE_SHOP_URL)
                t = numpy.random.exponential(MEAN_VISIT)
                time.sleep(t)
                #time.sleep(2)
                #self.driver.get(GOOGLE_SHOP_URL)

                self.my_log.debug('>start searching:%s',term)
                self.my_log.debug('Search for '+term)
                self.driver.find_element_by_id(input_shop_id).clear()
                self.driver.find_element_by_id(input_shop_id).send_keys(term)
                self.driver.find_element_by_id(
                    input_shop_id).send_keys(Keys.RETURN)
                time.sleep(5)
                self.log('measurement', 'google search', term)
                time.sleep(5)  # must sleep to wait for loading page
                html = self.driver.page_source.encode('utf8')  # need unicode for writing

                time.sleep(5)
                f_name = '_training'
                if training is False:  # this is testing
                    f_name = '_testing'
                file_name = self.save_html_page(
                    html, self.user_name, term + ".shopping" + f_name,saving=(not training))
                self.save_log(file_name, 'price')
                """
                    saving the list of links, prices to a new files email.prices.txt, format price file is:...
                    Searching term is@_@<term>
                    Average price is@_@@_@<ave_price>
                    <link>@_@<link_text>@_@<price>
                """
                file_namep = "training_" + self.user_name + PRICE_FILE
                if training is False:
                    file_namep = "testing_" + self.user_name + PRICE_FILE
                price_file = open(
                    os.path.join(self.log_file[:-4], file_namep), 'a')
                odict = price_utilities.get_all_products_prices_links(html)
                average_price = -1
                try:
                    average_price, _ = price_utilities.get_everage_price(html)
                except Exception as e:
                    average_price = 'NA'

                # write the content of items, prices
                price_file.write(
                    "=============================" + time.ctime() + "=================\n")
                price_file.write("Searching term is@_@" + term.strip() + "\n")
                price_file.write(
                    "Average price is@_@" + str(average_price).strip() + "\n")
                for k, v in odict.items():
                    price_file.write(
                        k.encode('utf-8').strip() + "@_@" + str(v).strip() + "\n")
                price_file.close()
                # saving data in to json file when do testing:

                all_data_dict = collections.OrderedDict()
                all_data_dict[USER_NAME] = self.user_name
                all_data_dict[SERIAL] = serial
                all_data_dict[AVERAGE_PRICE] = average_price
                all_data_dict[SEARCHING_TERM] = term.strip()
                all_data_dict[
                    PRICE_DATA] = odict
                if training is True:
                    url = self.driver.current_url
                    clicked_dict1 = self.click_on_links(
                        odict, price_condition, number_of_results_to_click)
                    all_data_dict[CLICKED_LINKS] = clicked_dict1
                    print 'CLICKED_LINKS:'
                    print all_data_dict[CLICKED_LINKS]
#                    self.my_log.debug('all_data_dict[CLICKED_LINKS]='+all_data_dict[CLICKED_LINKS])
                    try:
                        # click on link inside visited sites

                        self.my_log.debug('current url:%s',self.driver.current_url)
                        clicked_dict2 = self.click_links_in_visited_list(odict,average_price=average_price)
                        all_data_dict[CLICKED_LINKS_GDN] = clicked_dict2
                    except Exception as e:
                        print('Excecption:',e)
                        #print(self.driver.current_url)
                        print(e)
                if training is False:
                    self.my_log.debug('current url:%s',self.driver.current_url)
                    all_data_dict[CLICKED_LINKS_GDN] = self.click_links_in_visited_list(odict, train=False)
                    #self.my_log.debug('all_data_dict[CLICKED_LINKS_GDN]:'+all_data_dict[CLICKED_LINKS_GDN])
                    print 'gnd:'
                    #print 'all_data_dict[CLICKED_LINKS_GDN]'
                    #print all_data_dict[CLICKED_LINKS_GDN]
                all_data_dict['time'] = time.ctime()
                data_ = json.dumps(all_data_dict, ensure_ascii=False)
                with open(
                    os.path.join(self.log_file[:-4], 'json_' + file_namep), 'a',) as k:
                    k.write(data_.encode('utf-8'))
            except Exception, e:
                import logging
                #logging.exception('>Exception',e)
                print(e)
                #print(self.driver.current_url)
                self.log('error', 'google search personas', term)
            finally:
                print(
                    '===============ENDING SEARCH GOOGLE====================',self.user_name)
                if training is False:
                    self.my_log.critical(file_namep)
                    print(">>>>>>>>>>>", ultima_line,self.user_name)
                    with open(
                            os.path.join(self.log_file[:-4], file_namep), 'a') as f:
                        f.write(ultima_line)
            #time.sleep(30)
        return

    def click_links_in_visited_list(self, odict, train = True, no_click = False, average_price = 2000000):
        """click on a link if it is on visited website's list
            -- odict: dictionary of get_all_products_prices_links(html_content)
            -- train: default is true: True if this is training phase, False if testing phase
            -- if train is True: click on the link when link inside visted website list, otherwise not
            -- return a dictionary of links which are inside visited website list
            -- click on link if its price is > average price 20%
            default, not click on any link
        """
        average_price = average_price + average_price*0.2
        #self.load_shop_list()
        # get all the links
        clicked_link_dict = collections.OrderedDict()
        no_click = True
        if no_click is True:
            return clicked_link_dict
        links_dict = odict  # price_utilities.get_all_products_prices_links(html_content)
        links = [
            key for key in links_dict.keys()]  # .split("@_@")[0] {google.com@_@Google Search@_@20}, key is 20

        # check if any 'links' contain a website address from
        # self.visited_list
        if not self.visited_list:
            self.my_log.debug('>>>>cannot load visiting sites')
            #self.my_log.critical('Exception:')
        self.my_log.critical('>enter click_links_in_visited_list:%s',self.visited_list)
        self.my_log.debug('current url:%s',self.driver.current_url)
        _url = self.driver.current_url
        # only click 2 links in that
        nu = 0
        # click only if the link price is more than average
        for site in self.visited_list:
            if nu > 0:
                #break
                True
            #self.my_log.debug('site is %s',site)
            for link in links:
                #if price < average price, return

                if site in link:
                    if train is False:
                        clicked_link_dict[link] = links_dict[link]
                    if train is True:
                        if links_dict[link] < average_price:
                            return
                        self.my_log.debug('visit this %s',link)
                        if nu > 1:
                            #nu = 0
                            #break
                            True
                        try:
                            nu = nu + 1
                            self.my_log.debug('>>> For site:' + site)
                            # click on the link
                            if link.endswith('...'):
                                link = link[:-4].strip()
                            self.my_log.debug('visite step 1:1st click')
                            #self.driver.find
                            self.driver.find_elements_by_partial_link_text(
                                link.split("@_@")[-1])[-1].click()
                            time.sleep(5)
                            self.my_log.debug('visite step 2:2nd click')
                            try:
                                self.driver.find_elements_by_partial_link_text(
                                link.split("@_@")[-1])[-1].click()
                            except TimeoutException:
                                self.my_log.warning('Cannot load webpage. Continue')
                                self.driver.back()
                            time.sleep(5)
                            clicked_link_dict[link] = links_dict[link]
                            self.scrolling_in_website(
                                (numpy.random.exponential(MEAN_VISIT)))
                            time.sleep(2)
                            self.driver.back()
                            self.my_log.debug('Going back to %s', self.driver.current_url)
                        except:
                            self.my_log.exception('Cannot click on %s. Continue', link.split("@_@")[-1])
                            self.driver.get(_url)
                            break
            #break        #time.sleep(15)
                        #finally:
                        #    return clicked_link_dict
        return clicked_link_dict

    def click_on_links(self, odict, price_condition, number_of_results_to_click):
        """
            must write details here after code worked
            only run when training is true.
            odict -- dictionay of .....
            price_condition -- low, high, 3,10....
        """
        # get number_of_results_to_click (-th top cheapest or -th most expensive links and )
        # save to most_expensive
        most_expensive = price_utilities.get_top_n_most_expensive_product(
            odict,
            price_condition,
            number_of_link_to_click=number_of_results_to_click)
        # to store which links are click, and prices of those links
        clicked_link_dict = collections.OrderedDict()

        #print(most_expensive.items())

        most_expensive_links_file = open(
            "training_most_expensive_" + self.user_name + PRICE_FILE, 'a')
        most_expensive_links_file.write(most_expensive.keys()[0].encode('utf-8'))
        most_expensive_links_file.close()
        self.my_log.critical("Number of links to click is: %d",len(most_expensive))
        # DONE
        # DONE: if the website is on the visited list, click on it, for every site
        # load the list of visited websites: must be done before
        # this function is called

        # generate the waiting time
        # visit_time_array =
        # numpy.random.exponential(90,len(most_expensive)).tolist()
        print('for searched links')
        for k in most_expensive.keys():

            link_text = k.split('@_@')[-1].strip()
            if link_text.endswith('...'):
                link_text = link_text[:-4].strip()
            # print(link_text)
            print('click on:' + link_text)
            try:
                self.my_log.debug('first click')
                self.driver.find_elements_by_partial_link_text(
                    link_text)[-1].click()
                time.sleep(5)
                self.my_log.debug('2nd click')
                self.driver.find_elements_by_partial_link_text(link_text)[
                    -1].click()  # this is the trick of google, must click twice
                time.sleep(5)
                t = numpy.random.exponential(MEAN_VISIT)
                self.my_log.debug('stay in this site for: %d', t%30)
                self.scrolling_in_website(t)
                time.sleep(2)
                # add link to dict
                clicked_link_dict[k] = most_expensive[k]
                self.driver.back()
            except Exception, e:
                #print(e)
                #print(">exception!",e)
                #print(self.driver.current_url)
                self.my_log.exception('Exception when click on expensive/cheap/etc links')
        return clicked_link_dict

    def write_last_ending_line(self, file_name, previous_number=0):
        '''
        write the serial number line at the end of log file
        '''
        # write the serial number to the end of file
        file_name = "testing_" + self.user_name + PRICE_FILE
        # get the serial number, written from the previous time
        line = last_line(os.path.join(self.log_file[:-4], file_name))
        new_line = LOG_SEPARATE_LINE
        if line.startswith(LOG_SEPARATE_LINE) is False:
            new_line = LOG_SEPARATE_LINE + "@_@0"
        else:
            serial = int(line.split('@_@')[1])
            new_line = LOG_SEPARATE_LINE + "@_@" + \
                str(serial + 1) + "\n"
        with open(os.path.join(self.log_file[:-4], file_name), 'a') as f:
            # f.write(new_line)
            print('New line is:', new_line)

        # 18/12/2015 End
    # -END-16-Dec#####################

    def load_shop_list(self, file_):
        """loading file contains queyr for shopping"""
        try:
            print(self.user_name)
            f = open(file_)
            _list = []
            for l in f:
                if l.startswith('#'):
                    continue
                _list.append(l.strip())
            return _list
        except Exception, e:
            print("This is the guy:",self.user_name)
            raise e
        f.close()


def test():
    """
    """
    import sys
    sys.path

###from multiprocessing import Process


###def test_eco():
    ###user_name = "mericomanfrin@lab.imtlucca.it"
    ###password = 'imtlucca3078'
        #### sites = 'alexa/economics.personas.txt'
    ###sites = 'alexa/test_sites.txt'
####    shop = load_shop_list('alexa/test_shop.txt')
    ###b = GoogleAdsUnit(
        ###browser='firefox', log_file=user_name + ".txt", unit_id=1,
        ###treatment_id=1, headless=False, proxy=None)
    ###c = GoogleAdsUnit(
        ###browser='firefox', log_file=user_name + ".txt", unit_id=1,
        ###treatment_id=0, headless=False, proxy=None)
    ###shop = b.load_shop_list('alexa/test_shop.txt')
    ###b.login_google(user_name, password, dummy_login=False)
        #### b.visit_sites(sites)
    ###procs = []

    ###def proc_b(shop):
        ###b.search_for_measuring_price(shop)
        #### b.search_for_measuring_price(shop,training=False)
        #### b.search_for_measuring_price_testing_phase(shop)
        ###b.quit()

    ###def proc_c(shop):
        ###c.search_for_measuring_price(shop)
        #### c.search_for_measuring_price(shop,training=False)
        #### c.search_for_measuring_price_testing_phase(shop)
        ###c.quit()

    ###procs.append(Process(target=proc_b,
                         ###args=(shop,)))
    ###procs.append(Process(target=proc_c,
                         ###args=(shop,)))
    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)

#### test_eco()


###def test_luxury():
    ###user_name = "cherubinonapolitani@lab.imtlucca.it"
    ###password = 'imtlucca3077'
    #### sites = 'alexa/economics.personas.txt'
    ###sites = 'alexa/luxury.personas.txt'
    ###shop = load_shop_list('alexa/shop.txt')
    ###b = GoogleAdsUnit(
        ###browser='firefox', log_file=user_name + ".txt", unit_id=1,
        ###treatment_id=1, headless=True, proxy=None)
    ###c = GoogleAdsUnit(
        ###browser='firefox', log_file=user_name + ".txt", unit_id=1,
        ###treatment_id=0, headless=True, proxy=None)

    ###b.login_google(user_name, password)
    ###b.visit_sites(sites)
    ###procs = []

    ###def proc_b(shop):
        ###b.search_for_measurement_personas(shop)
        ###b.quit()

    ###def proc_c(shop):
        ###c.search_for_measurement_personas(shop)
        ###c.quit()

    ###procs.append(Process(target=proc_b,
                         ###args=(shop,)))
    ###procs.append(Process(target=proc_c,
                         ###args=(shop,)))
    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)

    #### b.search_for_measurement_personas(shop)
        #### c.search_for_measurement_personas(shop)
        #### b.quit()
        #### c.quit()


###def parallel():
    ###"""This is for different personas"""
    ###procs = []
    ###procs.append(Process(target=test_eco))
    ###procs.append(Process(target=test_luxury))
    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)


#### for i in range(0,4):
#### parallel()


###def test_personas_condition(
    ###user_name, password, sites, visit_site=True, traing_keywords="train.txt",
        ###test_keywords='alexa/shop.txt', condition="high"):
    ###'''
    ###must be in full path, i.e, alexa/economics.personas.txt \n
    ###user_name, password: username and password of account\n
    ###sites: list of websites to be visited\n
    ###visit_site: user will visit sites or not before search, True or False\n
    ###training_keywords: keywords for training phase\n
    ###test_keywords: keywords for testing phase\n


    ###'''
        #### user_name = "cherubinonapolitani@lab.imtlucca.it"
        #### password = 'imtlucca3077'
        #### sites = 'alexa/economics.personas.txt'
        #### sites = 'alexa/luxury.personas.txt'
        #### shop = load_shop_list('alexa/shop.txt') this is testing parth
    ###test_keywords = shop = load_shop_list(test_keywords)
    ###b = GoogleAdsUnit(
        ###browser='firefox', log_file=user_name + ".txt", unit_id=1,
        ###treatment_id=1, headless=False, proxy=None)
    ###c = GoogleAdsUnit(
        ###browser='firefox', log_file=user_name + ".txt", unit_id=1,
        ###treatment_id=0, headless=False, proxy=None)

    ###b.login_google(user_name, password)
    ###if visit_site is True:
        ###b.visit_sites(sites)
                #### b.visit_sites(sites)
                #### b.visit_sites(sites)
                #### b.visit_sites(sites)
        #### search for train keywords
    ###traing_keywords = load_shop_list(traing_keywords)
    ###b.search_for_measuring_price(traing_keywords, price_condition=condition)

    ###procs = []

    ###def proc_b(test_keywords):
        #### b.search_for_measurement_personas(shop)
        ###b.search_for_measuring_price(test_keywords, training=False)
        ###b.quit()

    ###def proc_c(test_keywords):
        #### c.search_for_measurement_personas(shop)
        ###c.search_for_measuring_price(test_keywords, training=False)
        ###c.quit()

    #### TESTING
    ###procs.append(Process(target=proc_b,
                         ###args=(test_keywords,)))
    ###procs.append(Process(target=proc_c,
                         ###args=(test_keywords,)))
    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)


###def parallel_gnd_testing():
    ###'''testing to visit gnd and non-gnd website, than get price of products'''
    ###procs = []
    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"EufrosinaCremonesi@lab.imtlucca.it", 'imtlucca3067', 'alexa/luxury_v_gdn59.links.txt',)))
        #### procs.append(Process(target=test_personas_condition, args=('bob',)))
    ###procs.append(Process(target=test_personas_condition,
                         ###args=("DonatellaPagnotto@lab.imtlucca.it", 'imtlucca3068', 'alexa/luxury_v.links.txt',)))
    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)


#### parallel_gnd_testing()
###def parallel_gnd_testing_6_accounts():
    ###'''
    ###testing to visit gnd and non-gnd website, than get price of products
    ###this time is repeatation of above one with bigger scale: 6 accounts
    ###'''

    ###procs = []
    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"EufrosinaCremonesi@lab.imtlucca.it", 'imtlucca3067', 'alexa/luxury_v_gdn59.links.txt',)))
    ###procs.append(Process(target=test_personas_condition,
                         ###args=("DonatellaPagnotto@lab.imtlucca.it", 'imtlucca3068', 'alexa/luxury_v.links.txt',)))

    ###procs.append(Process(target=test_personas_condition,
                         ###args=("NatalinoCalabrese@lab.imtlucca.it", 'imtlucca3029', 'alexa/luxury_v_gdn59.links.txt',)))
    ###procs.append(Process(target=test_personas_condition,
                         ###args=("IvaTrentino@lab.imtlucca.it", 'imtlucca3030', 'alexa/luxury_v.links.txt',)))

    ###procs.append(Process(target=test_personas_condition,
                         ###args=("MericoManfrin@lab.imtlucca.it", 'imtlucca3078', 'alexa/luxury_v_gdn59.links.txt',)))
    ###procs.append(Process(target=test_personas_condition,
                         ###args=("CristoforoPisano@lab.imtlucca.it", 'imtlucca3079', 'alexa/luxury_v.links.txt',)))

    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)


#### parallel_gnd_testing_6_accounts()
###def parallel_gnd_testing_5_accounts_games():
    ###'''
    ###testing to visit gnd and non-gnd website, than get price of products
    ###this is for topics about games
    ###here the luxy_ones does not surf any_more, just search
    ###'''

    ###procs = []
    #### these are for luxury_for ref_only --- with gdn#####
    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"EufrosinaCremonesi@lab.imtlucca.it", 'imtlucca3067', 'alexa/luxury_gnd_50_ads.links.txt',)))
        #### procs.append(Process(target=test_personas_condition, args=('bob',)))
        #### procs.append(Process(target=test_personas_condition,
        #### args=("DonatellaPagnotto@lab.imtlucca.it",'imtlucca3068','alexa/luxury_v.links.txt',)))
    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"NatalinoCalabrese@lab.imtlucca.it", 'imtlucca3029', 'alexa/luxury_gnd_50_ads.links.txt',)))
        #### procs.append(Process(target=test_personas_condition, args=("IvaTrentino@lab.imtlucca.it",'imtlucca3030','alexa/luxury_v.links.txt',)))
    #### end lux_reference__################

    #### start the economico part########
    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"ArtemisiaTrevisani@lab.imtlucca.it", 'imtlucca3031', 'alexa/game_no_gnd_50.links.txt',)))
    ###procs.append(Process(target=test_personas_condition,
                         ###args=("NiclaSal@lab.imtlucca.it", 'imtlucca3032', 'alexa/game_gdn_50.links.txt',)))

    ###procs.append(Process(target=test_personas_condition,
                         ###args=("ImmacolataFanucci@lab.imtlucca.it", 'imtlucca3033', 'alexa/game_no_gnd_50.links.txt',)))
    ###procs.append(Process(target=test_personas_condition,
                         ###args=("QuintiliaGiordano@lab.imtlucca.it", 'imtlucca3034', 'alexa/game_gdn_50.links.txt',)))
    ###procs.append(Process(target=test_personas_condition,
                         ###args=("BonifacioGenovesi@lab.imtlucca.it", 'imtlucca3035', 'alexa/game_gdn_50.links.txt',)))
    #### end##############################

    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)


#### parallel_gnd_testing_5_accounts_games()


###def main_test():
    ###user_name = "mericomanfrin@lab.imtlucca.it"
    ###password = 'imtlucca3078'
        #### sites = 'alexa/economics.personas.txt'
    ###sites = 'alexa/test_sites.txt'
    ###shop = load_shop_list('alexa/test_shop.txt')
    ###b = GoogleAdsUnit(
        ###browser='firefox', log_file=user_name + ".txt", unit_id=1,
        ###treatment_id=1, headless=True, proxy=None)
    ###c = GoogleAdsUnit(
        ###browser='firefox', log_file=user_name + ".txt", unit_id=1,
        ###treatment_id=0, headless=False, proxy=None)

    #### add one more luxury/economic user
        #### set up with new accounts
    ###b.login_google(user_name, password)
    ###b.load_visited_websites(sites)  # this is important, must do
    ###b.visit_sites(sites)  # visit list of websites
    ###procs = []

    ###def proc_b(shop):
        #### click on first 4 cheapest price products of search results
        #### load list of websites
        ###b.search_for_measuring_price(
            ###shop, price_condition='low', number_of_results_to_click=4)
        #### b.search_for_measuring_price(shop,training=False)

        ###b.quit()

    ###def proc_c(shop):
        ###c.search_for_measuring_price(shop)
        #### c.search_for_measuring_price(shop,training=False)

        ###c.quit()

        #### this part is for multiple-processing
    ###procs.append(Process(target=proc_b,
                         ###args=(shop,)))
    ###procs.append(Process(target=proc_c,
                         ###args=(shop,)))
    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)


###def simple_testing_2_accounts():
    ###'''
    ###testing to visit gnd and non-gnd website, than get price of products
    ###this time is repeatation of above one with bigger scale: 6 accounts
    ###'''

    ###procs = []
        #### test_personas_condition(user_name,password,sites,visit_site =
        #### True,traing_keywords = "train.txt", _shop='alexa/shop.txt')
    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"MarinoBellucci@lab.imtlucca.it", 'imtlucca00001', 'test/site_lux.txt', True, 'test/train_lux.txt', 'test/test.txt',
                         ###'high',)))
    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"CorneliaFolliero@lab.imtlucca.it", 'imtlucca00001', 'test/site_budget.txt', True, 'test/train_budget.txt',
                         ###'test/test.txt', 'low',)))

    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"ArnaldoFiorentino@lab.imtlucca.it", 'imtlucca00001', 'test/site_lux.txt', True, 'test/train_lux.txt',
                         ###'test/test.txt', 'high',)))
    ###procs.append(Process(target=test_personas_condition, args=(
                         ###"GeronimaEsposito@lab.imtlucca.it", 'imtlucca00001', 'test/site_budget.txt', True, 'test/train_budget.txt',
                         ###'test/test.txt', 'low',)))

    ###map(lambda x: x.start(), procs)
    ###map(lambda x: x.join(60 + 5), procs)


###if __name__ == "__main__":
    ###simple_testing_2_accounts()  # 1
#print(GoogleAdsUnit.load_visited_websites2())
#a = GoogleAdsUnit(
#        browser='chrome', log_file=None, unit_id=None,
#        treatment_id=1, headless=False, proxy=None)
#a.login_google('AriannaToscano@lab.imtlucca.it','imtlucca00001')
#a.self.visiting_sites = ['zappos.com']

#print GoogleAdsUnit.load_visited_websites2("/home/vino/AdFisher_Code/examples/experiment1/watch_lux_train_websites.txt")
