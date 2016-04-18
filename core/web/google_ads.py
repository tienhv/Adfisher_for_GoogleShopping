# This line of text does nothing
import time, re, os  # time.sleep, re.split, os,
import sys
from selenium import webdriver  # for running the driver on websites
from datetime import datetime  # for tagging log with datetime
from selenium.webdriver.common.keys import Keys  # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains  # to move mouse over
import numpy
# import browser_unit
import google_search
import price_utilities

# Google ad settings page class declarations



###TIEN
MEAN_VISIT = 90
####

input_shop_id = 'gbqfq'
GOOGLE_SHOP_URL = 'http://shopping.google.com/?&hl=en'
DEFAULT_CONDITION_CLICK_PRICE = 1  # click on the most expensive link
PRICE_FILE = '_price_sh.txt'

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


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class GoogleAdsUnit(google_search.GoogleSearchUnit):
    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        google_search.GoogleSearchUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        #         browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        self.isLogin = False
        self.user_name = "nologin"
        self.password = "nologin"
        self.personas = False
        self.visited_list = []
        self.driver.set_page_load_timeout(60)

    def opt_in(self):
        pass

    def opt_out(self):
        pass

    def create_folder(self, directory):
        """create folder to store all files: html, txt"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        return

    def login_google(self, username, password):
        """Login to Google with username and password"""
        try:
            print ('Enter logging function')
            google = 'http://www.google.com/ncr'
            self.driver.get(google)
            self.driver.get(self.base_url)
            self.driver.find_element_by_id("gb_70").click()
            self.driver.find_element_by_id("Email").clear()
            self.driver.find_element_by_id("Email").send_keys(username)
            self.driver.find_element_by_id("next").click()
            self.driver.find_element_by_id("Passwd").clear()
            self.driver.find_element_by_id("Passwd").send_keys(password)
            self.driver.find_element_by_id("signIn").click()

            self.isLogin = True  # set login is tru   e
            self.user_name = username
            self.password = password
            self.create_folder(self.user_name)
            self.log('treatment', 'login', username)
        except:
            self.log('error', 'logging in to google', username)
        time.sleep(3)
    

        ##############-START-16-Dec###################    
    def load_visited_websites(self, file_):

        f = open(file_, 'rt')
        for line in f:
            self.visited_list.append(line.strip())
        f.close()

    ####18/12/2015
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
        self.driver.set_page_load_timeout(30)
        for term in terms:
            time.sleep(5)
            print("Enter measurement function " + str(self.isLogin))
            try:
                self.driver.get(GOOGLE_SHOP_URL)
                print('start searching')
                self.driver.find_element_by_id(input_shop_id).clear()
                self.driver.find_element_by_id(input_shop_id).send_keys(term)
                self.driver.find_element_by_id(input_shop_id).send_keys(Keys.RETURN)
                time.sleep(5)
                self.log('measurement', 'google search', term)
                time.sleep(1)  # must sleep to wait for loading page
                html = self.driver.page_source.encode('utf8')  # need unicode for writing

                def create_new_file_name(email, term):  # folder, term is suffix
                    """
                    email: folder_name, a@imtluca.it/...term.*.html
                    """
                    import os
                    i = 0
                    if self.isLogin == False:
                        email = 'nologin'
                    name = email + "." + term + "." + str(i) + ".html"
                    while (os.path.exists(os.path.join(self.log_file[:-4], name))):
                        i = i + 1
                        name = email + "." + term + "." + str(i) + ".html"
                    ## write to log file
                    # file for
                    return name

                def save_html_page(html, email, term):
                    html_name = create_new_file_name(self.user_name, term)
                    print html_name
                    with open(os.path.join(self.log_file[:-4], html_name), 'w') as temp_file:
                        print('saving thml')
                        temp_file.write(html)
                    return html_name

                time.sleep(1)
                f_name = '_training'
                if training == False:  # this is testing
                    f_name = '_testing'
                file_name = save_html_page(html, self.user_name, term + ".shopping" + f_name)
                self.save_log(file_name, 'price')
                ################################
                """
                    saving the list of links, prices
                    to a new files email.prices_sh.txt
                    format price file is:
                    ======....
                    Searching term is@_@<term>
                    Average price is@_@@_@<ave_price>
                    <link>@_@<link_text>@_@<price>

                    TODO: add descriptive statistic on this file or separate file???
                """
                file_name = "training_" + self.user_name + PRICE_FILE
                if training == False:
                    file_name = "testing_" + self.user_name + PRICE_FILE
                price_file = open(file_name, 'a')
                odict = price_utilities.get_all_products_prices_links(html)
                average_price, _ = price_utilities.get_everage_price(html)

                # write the content of dictionary to file
                price_file.write("==============================================\n")
                price_file.write("Searching term is@_@" + term.strip() + "\n")
                price_file.write("Average price is@_@" + str(average_price).strip() + "\n")
                for k, v in odict.items():
                    price_file.write(k.encode('utf-8').strip() + "@_@" + str(v).strip() + "\n")
                price_file.close()

                #######CLICK on the most expensive item##################
                if training == True:
                    # get number_of_results_to_click (-th top cheapest or -th most expensive links and )
                    # save to most_expensive
                    most_expensive = price_utilities.get_top_n_most_expensive_product(odict,
                                                                                      price_condition,
                                                                                      number_of_results_to_click)
                    # store most expensive one in a file
                    # TODO: store average too
                    print(most_expensive.items())
                    most_expensive_links_file = open("training_most_expensive_" + self.user_name + PRICE_FILE, 'a')
                    most_expensive_links_file.write(most_expensive.keys()[0])
                    most_expensive_links_file.close()
                    # DONE
                    # TODO: if the website is on the visited list, click on it, for every site
                    # load the list of visited websites: must be done before this function is called

                    # generate the waiting time
                    # visit_time_array = numpy.random.exponential(90,len(most_expensive)).tolist()
                    print('for searched links')
                    for k in most_expensive.keys():

                        link_text = k.split('@_@')[-1].strip()
                        if link_text.endswith('...'):
                            link_text = link_text[:-4].strip()
                        # print(link_text)
                        print('click on:' + link_text)
                        try:
                            print('first click')
                            self.driver.find_elements_by_partial_link_text(link_text)[-1].click()
                            time.sleep(5)
                            print('2nd click')
                            self.driver.find_elements_by_partial_link_text(link_text)[
                                -1].click()  # this is the trick of google, must click twice
                            time.sleep(10)
                            # time.sleep(numpy.random.exponential(MEAN_VISIT))
                        except:
                            print("exception!")
                            print(self.driver.current_url)
                            pass
                        self.driver.back()

                    # to fix: find a way to discover if the link we click on it is inside the display network. as\a very simple idea you can first check if it's one of the visited website root name
                    try:
                        # get all the links
                        links_dict = odict  # price_utilities.get_all_products_prices_links(html_content)
                        links = [key for key in links_dict.keys()]  # .split("@_@")[0] {google.com@_@Google Search@_@20}
                        # check if any 'links' contain a website address from self.visited_list
                        print('for searched SITES')
                        for site in self.visited_list:

                            # print 'x'
                            # TODO: save this info to file
                            for link in links:
                                if site in link:
                                    print('go on: ' + site)
                                    # click on the link
                                    if link.endswith('...'):
                                        link = link[:-4].strip()
                                    print('1st click')
                                    self.driver.find_elements_by_partial_link_text(link.split("@_@")[-1]).click()
                                    time.sleep(5)
                                    print('2nd click')
                                    self.driver.find_elements_by_partial_link_text(link.split("@_@")[-1]).click()
                                    time.sleep(10)
                                    # time.sleep(numpy.random.exponential(MEAN_VISIT))
                                    self.driver.back()
                    except Exception as e:
                        print('Excecption:')
                        print(self.driver.current_url)
                        print(e)
                        pass
            except Exception, e:
                import logging
                logging.exception('exception')
                print(self.driver.current_url)
                self.log('error', 'google search personas', term)
        return

        #####18/12/2015 End

    ##############-END-16-Dec#####################

    def go_to_cnn(self):
        """Login to Google with username and password"""
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("http://cnn.com")
            self.log('treatment', 'login to google', username)
        except:
            self.log('error', 'logging in to google', username)

    def set_gender(self, gender):
        pass

    def set_age(self, age):
        """Set age on Google Ad Settings page"""
        pass

    def set_language(self, language):
        """Set language on Google Ad Settings page"""
        
        #    self.log('treatment', 'language', language)
        pass

    def remove_interest(self, pref):
        """Remove interests containing pref on the Google Ad Settings page"""
        
        #    self.log('treatment', 'remove interest (' + pref + ')', "@|".join(rem))
        pass

    def add_interest_ongoogle(self, pref, count=1, signedin=0):
        pass
    #         except:
    #             print "Error setting interests containing '%s'. Maybe no interests match this keyword." %(pref)
    #             self.log('error', 'adding interest', pref)

    def add_interest(self, pref, count=1, signedin=0):
        pass

    #         except:
    #             print "Error setting interests containing '%s'. Maybe no interests match this keyword." %(pref)
    #             self.log('error', 'adding interest', pref)


    def get_gender(self):
        
        #    self.log('measurement', 'gender', inn)
        pass

    def get_age(self):
        pass

    def get_language(self):
        pass

    def get_interests(self, text="interests"):
        pass

    def collect_ads(self, reloads, delay, site, file_name=None):
        pass

    def save_ads_fox(self, file):
        pass

    def save_ads_bloomberg(self, file):
        pass

    def save_ads_reuters(self, file):
        pass

    def save_ads_guardian(self, file):
        pas

    def save_ads_toi(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://timesofindia.indiatimes.com/international-home")
        time.sleep(10)
        tim = str(datetime.now())
        frame = driver.find_element_by_xpath(".//iframe[@id='ad-left-timeswidget']")

        def scroll_element_into_view(driver, element):
            """Scroll element into view"""
            y = element.location['y']
            driver.execute_script('window.scrollTo(0, {0})'.format(y))

        scroll_element_into_view(driver, frame)
        print frame
        driver.switch_to.frame(frame)
        ads = driver.find_elements_by_css_selector("html body table tbody tr td table")
        for ad in ads:
            aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
            bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
            t = aa[0].get_attribute('innerHTML')
            l = aa[1].get_attribute('innerHTML')
            b = bb[0].get_attribute('innerHTML')
            ad = strip_tags(tim + "@|" + t + "@|" + l + "@|" + b).encode("utf8")
            self.log('measurement', 'ad', ad)
        driver.switch_to.default_content()

    def save_ads_bbc(self, file):
        pass


    def load_shop_list(self, file_):
        """loading file contains queyr for shopping"""
        try:
            f = open(file_)
            _list = []
            for l in f:
                if l.startswith('#'):
                    continue
                _list.append(l.strip())
            return _list
        except Exception, e:
            raise e
        f.close()


from multiprocessing import Process


def test_eco():
    user_name = "mericomanfrin@lab.imtlucca.it"
    password = 'imtlucca3078'
	# sites = 'alexa/economics.personas.txt'
    sites = 'alexa/test_sites.txt'
#    shop = load_shop_list('alexa/test_shop.txt')
    b = GoogleAdsUnit(browser='firefox', log_file=user_name + ".txt", unit_id=1,
                      treatment_id=1, headless=False, proxy=None)
    c = GoogleAdsUnit(browser='firefox', log_file=user_name + ".txt", unit_id=1,
                      treatment_id=0, headless=False, proxy=None)
    shop = b.load_shop_list('alexa/test_shop.txt')
    b.login_google(user_name, password)
	# b.visit_sites(sites)
    procs = []

    def proc_b(shop):
        b.search_for_measuring_price(shop)
        # b.search_for_measuring_price(shop,training=False)
        # b.search_for_measuring_price_testing_phase(shop)
        b.quit()

    def proc_c(shop):
        c.search_for_measuring_price(shop)
        # c.search_for_measuring_price(shop,training=False)
        # c.search_for_measuring_price_testing_phase(shop)
        c.quit()

    procs.append(Process(target=proc_b,
                         args=(shop,)))
    procs.append(Process(target=proc_c,
                         args=(shop,)))
    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)

# test_eco()
def test_luxury():
    user_name = "cherubinonapolitani@lab.imtlucca.it"
    password = 'imtlucca3077'
    # sites = 'alexa/economics.personas.txt'
    sites = 'alexa/luxury.personas.txt'
    shop = load_shop_list('alexa/shop.txt')
    b = GoogleAdsUnit(browser='firefox', log_file=user_name + ".txt", unit_id=1,
                      treatment_id=1, headless=True, proxy=None)
    c = GoogleAdsUnit(browser='firefox', log_file=user_name + ".txt", unit_id=1,
                      treatment_id=0, headless=True, proxy=None)

    b.login_google(user_name, password)
    b.visit_sites(sites)
    procs = []

    def proc_b(shop):
        b.search_for_measurement_personas(shop)
        b.quit()

    def proc_c(shop):
        c.search_for_measurement_personas(shop)
        c.quit()

    procs.append(Process(target=proc_b,
                         args=(shop,)))
    procs.append(Process(target=proc_c,
                         args=(shop,)))
    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)

    # b.search_for_measurement_personas(shop)
	# c.search_for_measurement_personas(shop)
	# b.quit()
	# c.quit()


def parallel():
    """This is for different personas"""
    procs = []
    procs.append(Process(target=test_eco))
    procs.append(Process(target=test_luxury))
    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)


# for i in range(0,4):
# parallel()



def test_personas_condition(user_name, password, sites, visit_site=True, traing_keywords="train.txt",
                            test_keywords='alexa/shop.txt', condition="high"):
    '''
    must be in full path, i.e, alexa/economics.personas.txt \n
    user_name, password: username and password of account\n
    sites: list of websites to be visited\n
    visit_site: user will visit sites or not before search, True or False\n
    training_keywords: keywords for training phase\n
    test_keywords: keywords for testing phase\n
    
    
    '''
	# user_name = "cherubinonapolitani@lab.imtlucca.it"
	# password = 'imtlucca3077'
	# sites = 'alexa/economics.personas.txt'
	# sites = 'alexa/luxury.personas.txt'
	# shop = load_shop_list('alexa/shop.txt') this is testing parth
    test_keywords = shop = load_shop_list(test_keywords)
    b = GoogleAdsUnit(browser='firefox', log_file=user_name + ".txt", unit_id=1,
                      treatment_id=1, headless=False, proxy=None)
    c = GoogleAdsUnit(browser='firefox', log_file=user_name + ".txt", unit_id=1,
                      treatment_id=0, headless=False, proxy=None)

    b.login_google(user_name, password)
    if visit_site is True:
        b.visit_sites(sites)
		# b.visit_sites(sites)
		# b.visit_sites(sites)
		# b.visit_sites(sites)
	# search for train keywords
    traing_keywords = load_shop_list(traing_keywords)
    b.search_for_measuring_price(traing_keywords, price_condition=condition)

    procs = []

    def proc_b(test_keywords):
        # b.search_for_measurement_personas(shop)
        b.search_for_measuring_price(test_keywords, training=False)
        b.quit()

    def proc_c(test_keywords):
        # c.search_for_measurement_personas(shop)
        c.search_for_measuring_price(test_keywords, training=False)
        c.quit()

    # TESTING
    procs.append(Process(target=proc_b,
                         args=(test_keywords,)))
    procs.append(Process(target=proc_c,
                         args=(test_keywords,)))
    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)


def parallel_gnd_testing():
    '''testing to visit gnd and non-gnd website, than get price of products'''
    procs = []
    procs.append(Process(target=test_personas_condition, args=(
    "EufrosinaCremonesi@lab.imtlucca.it", 'imtlucca3067', 'alexa/luxury_v_gdn59.links.txt',)))
	# procs.append(Process(target=test_personas_condition, args=('bob',)))
    procs.append(Process(target=test_personas_condition,
                         args=("DonatellaPagnotto@lab.imtlucca.it", 'imtlucca3068', 'alexa/luxury_v.links.txt',)))
    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)


# parallel_gnd_testing()
def parallel_gnd_testing_6_accounts():
    '''
    testing to visit gnd and non-gnd website, than get price of products
    this time is repeatation of above one with bigger scale: 6 accounts
    '''

    procs = []
    procs.append(Process(target=test_personas_condition, args=(
    "EufrosinaCremonesi@lab.imtlucca.it", 'imtlucca3067', 'alexa/luxury_v_gdn59.links.txt',)))
    procs.append(Process(target=test_personas_condition,
                         args=("DonatellaPagnotto@lab.imtlucca.it", 'imtlucca3068', 'alexa/luxury_v.links.txt',)))

    procs.append(Process(target=test_personas_condition,
                         args=("NatalinoCalabrese@lab.imtlucca.it", 'imtlucca3029', 'alexa/luxury_v_gdn59.links.txt',)))
    procs.append(Process(target=test_personas_condition,
                         args=("IvaTrentino@lab.imtlucca.it", 'imtlucca3030', 'alexa/luxury_v.links.txt',)))

    procs.append(Process(target=test_personas_condition,
                         args=("MericoManfrin@lab.imtlucca.it", 'imtlucca3078', 'alexa/luxury_v_gdn59.links.txt',)))
    procs.append(Process(target=test_personas_condition,
                         args=("CristoforoPisano@lab.imtlucca.it", 'imtlucca3079', 'alexa/luxury_v.links.txt',)))

    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)


# parallel_gnd_testing_6_accounts()
def parallel_gnd_testing_5_accounts_games():
    '''
    testing to visit gnd and non-gnd website, than get price of products
    this is for topics about games
    here the luxy_ones does not surf any_more, just search
    '''

    procs = []
    ####these are for luxury_for ref_only --- with gdn#####
    procs.append(Process(target=test_personas_condition, args=(
    "EufrosinaCremonesi@lab.imtlucca.it", 'imtlucca3067', 'alexa/luxury_gnd_50_ads.links.txt',)))
	# procs.append(Process(target=test_personas_condition, args=('bob',)))
	# procs.append(Process(target=test_personas_condition, args=("DonatellaPagnotto@lab.imtlucca.it",'imtlucca3068','alexa/luxury_v.links.txt',)))
    procs.append(Process(target=test_personas_condition, args=(
    "NatalinoCalabrese@lab.imtlucca.it", 'imtlucca3029', 'alexa/luxury_gnd_50_ads.links.txt',)))
	# procs.append(Process(target=test_personas_condition, args=("IvaTrentino@lab.imtlucca.it",'imtlucca3030','alexa/luxury_v.links.txt',)))
    #####end lux_reference__################

    ###start the economico part########
    procs.append(Process(target=test_personas_condition, args=(
    "ArtemisiaTrevisani@lab.imtlucca.it", 'imtlucca3031', 'alexa/game_no_gnd_50.links.txt',)))
    procs.append(Process(target=test_personas_condition,
                         args=("NiclaSal@lab.imtlucca.it", 'imtlucca3032', 'alexa/game_gdn_50.links.txt',)))

    procs.append(Process(target=test_personas_condition,
                         args=("ImmacolataFanucci@lab.imtlucca.it", 'imtlucca3033', 'alexa/game_no_gnd_50.links.txt',)))
    procs.append(Process(target=test_personas_condition,
                         args=("QuintiliaGiordano@lab.imtlucca.it", 'imtlucca3034', 'alexa/game_gdn_50.links.txt',)))
    procs.append(Process(target=test_personas_condition,
                         args=("BonifacioGenovesi@lab.imtlucca.it", 'imtlucca3035', 'alexa/game_gdn_50.links.txt',)))
    ###end##############################

    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)


# parallel_gnd_testing_5_accounts_games()


def main_test():
    user_name = "mericomanfrin@lab.imtlucca.it"
    password = 'imtlucca3078'
	# sites = 'alexa/economics.personas.txt'
    sites = 'alexa/test_sites.txt'
    shop = load_shop_list('alexa/test_shop.txt')
    b = GoogleAdsUnit(browser='firefox', log_file=user_name + ".txt", unit_id=1,
                      treatment_id=1, headless=True, proxy=None)
    c = GoogleAdsUnit(browser='firefox', log_file=user_name + ".txt", unit_id=1,
                      treatment_id=0, headless=False, proxy=None)

    # add one more luxury/economic user
	# set up with new accounts
    b.login_google(user_name, password)
    b.load_visited_websites(sites)  # this is important, must do
    b.visit_sites(sites)  # visit list of websites
    procs = []

    def proc_b(shop):
        # click on first 4 cheapest price products of search results
        # load list of websites
        b.search_for_measuring_price(shop, price_condition='low', number_of_results_to_click=4)
        # b.search_for_measuring_price(shop,training=False)

        b.quit()

    def proc_c(shop):
        c.search_for_measuring_price(shop)
        # c.search_for_measuring_price(shop,training=False)

        c.quit()

	# this part is for multiple-processing
    procs.append(Process(target=proc_b,
                         args=(shop,)))
    procs.append(Process(target=proc_c,
                         args=(shop,)))
    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)


def simple_testing_2_accounts():
    '''
    testing to visit gnd and non-gnd website, than get price of products
    this time is repeatation of above one with bigger scale: 6 accounts
    '''

    procs = []
	# test_personas_condition(user_name,password,sites,visit_site = True,traing_keywords = "train.txt", _shop='alexa/shop.txt')
    procs.append(Process(target=test_personas_condition, args=(
    "MarinoBellucci@lab.imtlucca.it", 'imtlucca00001', 'test/site_lux.txt', True, 'test/train_lux.txt', 'test/test.txt',
    'high',)))
    procs.append(Process(target=test_personas_condition, args=(
    "CorneliaFolliero@lab.imtlucca.it", 'imtlucca00001', 'test/site_budget.txt', True, 'test/train_budget.txt',
    'test/test.txt', 'low',)))

    procs.append(Process(target=test_personas_condition, args=(
    "ArnaldoFiorentino@lab.imtlucca.it", 'imtlucca00001', 'test/site_lux.txt', True, 'test/train_lux.txt',
    'test/test.txt', 'high',)))
    procs.append(Process(target=test_personas_condition, args=(
    "GeronimaEsposito@lab.imtlucca.it", 'imtlucca00001', 'test/site_budget.txt', True, 'test/train_budget.txt',
    'test/test.txt', 'low',)))


    map(lambda x: x.start(), procs)
    map(lambda x: x.join(60 + 5), procs)


if __name__ == "__main__":
    simple_testing_2_accounts()  # 1