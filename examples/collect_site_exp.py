import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_ads               # interacting with Google ads and Ad Settings
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.demo.txt'
site_file = 'alexa/shop.txt'

"""####
Collect the top website, according to the input

"""
def make_browser(unit_id, treatment_id):
    b = web.google_ads.GoogleAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
                                     treatment_id=treatment_id, headless=True, proxy = None)
    return b

# Control Group treatment
def control_treatment(unit):
    unit.opt_in()
    unit.set_gender('f')
    unit.set_age(22)
    unit.set_language('English')
    unit.visit_sites(site_file)

# Experimental Group treatment
def exp_treatment(unit):
    unit.opt_in()
    unit.add_interest('basketball')
    unit.add_interest('dating')
    unit.remove_interest('basketball')
    unit.visit_sites(site_file)


# Measurement - Collects ads
def measurement(unit):
    unit.get_gender()
    unit.get_age()
    unit.get_language()
    unit.get_interests()
    unit.collect_ads(reloads=2, delay=5, site='bbc')


# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors
def load_results():
    pass

def test_stat(observed_values, unit_assignments):
    pass


def test_collect_site():
    
    top_sites = "http://www.alexa.com/topsites"
    #web.pre_experiment.alexa.collect_sites(make_browser, num_sites=25, output_file=site_file,
    #                                       alexa_link=top_sites)
    titan = 'http://www.alexa.com/topsites/category/Top/Shopping/Jewelry/Wedding/Rings/Titanium'
    web.pre_experiment.alexa.collect_sites(make_browser, num_sites=16, output_file=site_file,
                                           alexa_link=titan)    
#191 website
#each site, search for 



def run_collect_site():
    luxury_file = 'alexa/luxury.personas.txt'
    economic_file = 'alexa/economics.personas.txt'    
    game_toy = 'http://www.alexa.com/topsites/category/Top/Shopping/Toys_and_Games' #104 site
    auction = 'http://www.alexa.com/topsites/category/Top/Shopping/Auctions' #162
    
    web.pre_experiment.alexa.collect_sites(make_browser, num_sites=91, output_file=economic_file,
                                           alexa_link=game_toy)
    web.pre_experiment.alexa.collect_sites(make_browser, num_sites=100, output_file=economic_file,
                                           alexa_link=auction)
    
    luxury_wath ='http://www.alexa.com/topsites/category/Top/Shopping/Jewelry/Watches/Luxury' #52
    diamond = 'http://www.alexa.com/topsites/category/Top/Shopping/Jewelry/Diamonds' #69
    wedding_ring = 'http://www.alexa.com/topsites/category/Top/Shopping/Jewelry/Wedding/Rings'#70
    
    
    web.pre_experiment.alexa.collect_sites(make_browser, num_sites=52, output_file=luxury_file,
                                           alexa_link=luxury_wath)
    
    web.pre_experiment.alexa.collect_sites(make_browser, num_sites=69, output_file=luxury_file,
                                           alexa_link=diamond)
    web.pre_experiment.alexa.collect_sites(make_browser, num_sites=70, output_file=luxury_file,
                                           alexa_link=wedding_ring)    
    return

def create_query_files():
    """this function does not work because url is not normalized"""
    import tldextract
    luxury_file = 'alexa/luxury.personas.txt'
    economic_file = 'alexa/economics.personas.txt'        
    def make_file(file_name):
        f1 = open(file_name,'r')
        f2 = open(file_name[:-4] + ".query.txt",'w')
        for l in f1:
            try:
                s = tldextract.extract("http://"+l.strip()).domain
                #s = l.split('/')[0].split('.')[-2]
                
                f2.write(l.strip() +"@"+s+"\n")
            except Exception, e:
                print(e)
                print(l)
        f2.close()
        f1.close()
    make_file(luxury_file)
    make_file(economic_file)
 
#Run by order    
#run_collect_site()
#create_query_files(): not run

def run_collect_site_2():
    """collect luxury watche products """
    luxury_file = 'alexa/luxury.watch.txt'
    economic_file = 'alexa/game_sites.txt'    
    game_toy = 'http://www.alexa.com/topsites/category/Top/Shopping/Toys_and_Games/Games' #>404 site
    #auction = 'http://www.alexa.com/topsites/category/Top/Shopping/Auctions' #162
    print('I am here')
    web.pre_experiment.alexa.collect_sites(make_browser, num_sites=300, output_file=economic_file,
                                           alexa_link=game_toy)
    #web.pre_experiment.alexa.collect_sites(make_browser, num_sites=100, output_file=economic_file,
    #                                       alexa_link=auction)
    
    #luxury_wath ='http://www.alexa.com/topsites/category/Top/Shopping/Jewelry/Watches/Luxury' #52
    #diamond = 'http://www.alexa.com/topsites/category/Top/Shopping/Jewelry/Diamonds' #69
    #wedding_ring = 'http://www.alexa.com/topsites/category/Top/Shopping/Jewelry/Wedding/Rings'#70
    
    
    #web.pre_experiment.alexa.collect_sites(make_browser, num_sites=52, output_file=luxury_file,
    #                                       alexa_link=luxury_wath)
    
    #web.pre_experiment.alexa.collect_sites(make_browser, num_sites=69, output_file=luxury_file,
    #                                      alexa_link=diamond)
    #web.pre_experiment.alexa.collect_sites(make_browser, num_sites=70, output_file=luxury_file,
    #                                       alexa_link=wedding_ring)    
    return
print("I am running here")
run_collect_site_2()

