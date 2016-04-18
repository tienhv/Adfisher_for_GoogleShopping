#only for testing, no training at all
import sys
import os
sys.path.append("../core")          # files from the core
import web.pre_experiment.alexa     # collecting top sites from alexa
# import web.google_ads               # interacting with Google ads and Ad
# Settings
#import converter.reader             # read log and create feature vectors
#import analysis.statistics          # statistics for significance testing
import my_adfisher
# import web.google_search_personalize
import web.my_google_ads
log_file = 'experimence_pricing_3.txt'
#log_file = 'experiment_03_ny1_2_shoes.txt'
site_file = 'demo.txt'
#account_file = 'san_acc.txt'
account_file = 'experiment1/accounts_test.txt'
NO_EMAIL = 'no_email'
NO_PASSWORD = 'no_password'
SEPARATOR = '____'
import time



# ==== logging
import logging
from rainbow_logging_handler import RainbowLoggingHandler

FORMAT = "[%(asctime)s] %(levelname)s - %(name)s %(funcName)s():%(lineno)d\t%(message)s"

f = open('experiment1/pricing_logging_2.log','a+')

handler_ = RainbowLoggingHandler(sys.stdout)
handler_2 = RainbowLoggingHandler(f)

formatter = logging.Formatter(FORMAT)
fhandler = logging.FileHandler("experiment1/pricing_logging.log")
fhandler.setFormatter(FORMAT)
fhandler.setLevel(level=logging.DEBUG)

logging.getLogger().setLevel(level=logging.DEBUG)
logging.getLogger().addHandler(handler_)
logging.getLogger().addHandler(handler_2)
logging.getLogger().addHandler(fhandler)
logging.getLogger("selenium").setLevel(logging.WARNING)

my_log = logging.getLogger(__name__)

#my_log.addHandler(logging.FileHandler("pricing_logging.log"))
#my_log.addHandler(logging.FileHandler("experiment1/pricing_logging.log"))

# ====

def make_browser(unit_id, treatment_id, configuration):
    p = None
    if 'no_proxy' not in configuration.split(SEPARATOR)[-1].strip():
        p = configuration.split(SEPARATOR)[-1].strip()
    b = web.my_google_ads.GoogleAdsUnit(
        browser='firefox', log_file=log_file, unit_id=unit_id,
        treatment_id=treatment_id, headless=False, proxy=p)
    return b

# Control Group treatment


def load_accounts(file_name):
    """Reading account configutarions from file_name.
    Args:
        -- file_name: full path to configuration file
    return:
        -- []
        -- or a list contains all configuration. each element is one account
            configuration
    """
    persons = []
    try:
        f = open(file_name, 'r')
        for line in f:
            if line.startswith('#') or line.startswith(' '):
                continue
            if len(line) <=1:
                continue
            persons.append(line.strip())
        return persons
    except:
        my_log.exception('Error when reading accounts')
        sys.exit(1)

#   in the control experiment function,
#   pass all needed parameters to it
#
#


def control_treatment_nothing(unit, configuration):
    user_name = configuration.split(SEPARATOR)[0].strip()
    password = configuration.split(SEPARATOR)[1].strip()
    #print(">>>pass:",password)
    if password == NO_PASSWORD:
        control_treatment_2(unit, configuration)
        return
    control_treatment(unit, configuration)


def control_treatment(unit, configuration):
    user_name = configuration.split(SEPARATOR)[0].strip()
    password = configuration.split(SEPARATOR)[1].strip()
    training_terms = unit.load_shop_list(
        configuration.split(SEPARATOR)[3].strip())
    click_condition = configuration.split(SEPARATOR)[4].strip()
    sites = configuration.split(SEPARATOR)[2].strip()
    print(configuration.split(SEPARATOR)[0] + '-username:', user_name)
    print(configuration.split(SEPARATOR)[0] + '-password:', password)
    print(configuration.split(SEPARATOR)[0] + '-training:', training_terms)
    print(configuration.split(SEPARATOR)[0] + '-click:', click_condition)
    print(configuration.split(SEPARATOR)[0] + '-site:', sites)
    print(configuration.split(SEPARATOR)[0] + '-proxy:', configuration.split(SEPARATOR)[-1].strip())
    unit.login_google(user_name, password)
    unit.load_visited_websites(sites)
    #unit.visit_sites(sites)
    #unit.search_for_measuring_price(
    #    training_terms, price_condition=click_condition)


def control_treatment_2(unit, configuration):
    user_name = configuration.split(SEPARATOR)[0].strip()
    password = configuration.split(SEPARATOR)[1].strip()
    unit.login_google(user_name, password, dummy_login=True)


def measurement(unit, configuration):
    print(">>>>>>Enter measurement function, Will sleep for 10 minutes from now")    
    #time.sleep(600)# this one is prevention of google banning of activity
    # here enter the measurement function
    testing_terms = unit.load_shop_list(
        configuration.split(SEPARATOR)[5].strip())
    print(configuration.split(SEPARATOR)
          [0] + "-Tesing term is:", testing_terms)
    unit.search_for_measuring_price(testing_terms, training=False)
    time.sleep(10)


# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()


#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors


def load_results():
    pass


def test_stat(observed_values, unit_assignments):
    pass
#------------------------------------------------------------------------------

def run(accounts):
    print("Start woring here")
    my_adfisher.do_experiment(
        make_unit=make_browser, treatments=[
            control_treatment_nothing],
        measurement=measurement, end_unit=cleanup_browser,
        load_results=load_results, test_stat=test_stat, ml_analysis=False,
        num_blocks=1, num_units=len(accounts), timeout=108000, #time out is wating time of each process, this is 3 hours
        log_file=log_file, exp_flag=True, analysis_flag=False,
        treatment_names=["t1", "t2","t3","t4"], account_list=accounts)

account_list = load_accounts(account_file)  # this is configuration
print(account_list)
run(account_list)
f.close()
