#from bs4 import BeautifulSoup
import jellyfish
#import urlparse
import price_utilities
from scipy.stats import kendalltau
class Measurements():
    """
    Calculates edit distance and jaccard distance
    get all links
    """        
    
    @staticmethod
    def get_all_links(file1):
        '''
        get all links from the file1
        '''        
        links = []
        html_content = open(file1,'rt')
        html = html_content.read()#.encode('utf-8',errors='ignore')        
        #print(html)
        prices_links_dict = price_utilities.get_all_products_prices_links(
                                                                    html)
        #print prices_links_dict
        for k, v in prices_links_dict.items():
            links.append(k.split("@_@")[0])
        return links 

    @staticmethod
    def get_all_links_prices(file1):
        '''
        get all links from the file1
        '''        
        links = []
        prices =[]
        html_content = open(file1,'rt')
        html = html_content.read()#.encode('utf-8',errors='ignore')        
        #print(html)
        prices_links_dict = price_utilities.get_all_products_prices_links(
                                                                    html)
        #print prices_links_dict
        for k, v in prices_links_dict.items():
            links.append(k.split("@_@")[0])
            prices.append(v)            
        return links, prices
    
    @staticmethod
    def pages_to_alphabet(pages):
        s = set()
        for page in pages:
            links = Measurements.get_all_links(page)
            for l in links:
                s.add(l)
        alph = {}
        for i, url in enumerate(s):
            alph[url] = chr(i + 96)
        return alph
    @staticmethod
    def link_to_set(page):
        #s = set()
        links = Measurements.get_all_links(page)
        s = set(links)
        return s
    @staticmethod
    def page_to_string(page, alph):
        s = ''
        links = Measurements.get_all_links(page)
        for l in links:
            s += alph[l]
        return s	
    @staticmethod
    def damerau_levenshtein_distance_cal(str1, str2):
        str1 = unicode(str1, 'utf-8',errors='ignore')
        str2 = unicode(str2, 'utf-8',errors='ignore')
        return jellyfish.damerau_levenshtein_distance(str1, str2)
   
        
    @staticmethod
    def compare_pages(page1, page2):
        """compare two_page, generate jaccard index, and damerau_levenshtein_distance_cal """		
        s1 = Measurements.link_to_set(page1)
        s2 = Measurements.link_to_set(page2)

        alph = Measurements.pages_to_alphabet([page1, page2])
        print ("From page1:"+page1)
        str1 = Measurements.page_to_string(page1, alph)
        print ("From page2:"+page2)
        str2 = Measurements.page_to_string(page2, alph)
        # so sanh coi cai nay giong cai kia bao nhieu phan tram
        if len(s1) > len(s2):
            j = float(len(s1.intersection(s2)))/len(s1)
        else:
            j = float(len(s2.intersection(s1)))/len(s2)
        e  = Measurements.damerau_levenshtein_distance_cal(str1, str2)        
        return j, e	
    @staticmethod
    def compare_pages_links_prices(page1, page2):
        """compare two_page, generate indexes"""
        (links1, prices1)= Measurements.get_all_links_prices(page1)
        (links2, prices2)= Measurements.get_all_links_prices(page2)
       
        s1=set()
        for i in range(len(links1)):
            s1.add(links1[i]+'&&&'+str(prices1[i]))
        s2=set()
        for i in range(len(links2)):
            s2.add(links2[i]+'&&&'+str(prices2[i]))        
        #  s1 = Measurements.link_to_set(page1)
        # s2 = Measurements.link_to_set(page2)

        alph = Measurements.pages_to_alphabet([page1, page2])
        print ("From page1:"+page1)
        str1 = Measurements.page_to_string(page1, alph)
        print ("From page2:"+page2)
        str2 = Measurements.page_to_string(page2, alph)
        # so sanh coi cai nay giong cai kia bao nhieu phan tram
        # day khong phai la jaccard index theo dinh nghia, update: nhan xet sai
        # this is not Jaccard index by denifition - inspired from Hannak paper
        inter = None        
        inter2 = None

        inter=s1.difference(s2)
        inter2=s2.difference(s1)
        
        if len(s1) > len(s2):
            
            j = float(len(s1.intersection(s2)))/len(s1)
        else:
            j = float(len(s2.intersection(s1)))/len(s2)
        e  = Measurements.damerau_levenshtein_distance_cal(str1, str2)
        
        return j, e, inter,inter2

    @staticmethod
    def ncdg(file_, file_list):
        """
        Calculate the ncdg\n
        file_: file to be calculated\n
        file_list: the list of reference file\n
        URL{https://www.kaggle.com/wiki/NormalizedDiscountedCumulativeGain}
        """
        return price_utilities.ncdg_calculate(file_,file_list)
        
    
    @staticmethod
    def editdist_and_kendalltau(page1, page2):
        """
        return damerau_levenshtein_distance and kendall_tau values \n
        page1, page2: full path to html page on local disk
        """
        alph = Measurements.pages_to_alphabet([page1, page2])
        str1 = Measurements.page_to_string(page1, alph)
        str2 = Measurements.page_to_string(page2, alph)
        str1 = unicode(str1, 'utf-8',errors='ignore')
        str2 = unicode(str2, 'utf-8',errors='ignore')
        l1 = [a for a in str1]
        l2 = [a for a in str2]
        while len(l1) < len(l2): l1.append('null')
        while len(l2) < len(l1): l2.append('null')
        j, e = Measurements.compare_pages(page1, page2) #jaccard index and damerau_levenshtein_distance_cal
        return (j, e, kendalltau(l1, l2)[0]) #jaccard index, damerau, and kendall-tau 
    @staticmethod
    def compare_pages_mismatch(page1, page2):
        """compare two_page, generate indexes"""
        #read file1
        html_file = open(page1,'rt')
        html = html_file.read()       
        #format of the dictionary: {link@_@link_text:price}
        #key: link@_@text_of_link, value:price
        prices_links_dict1 = price_utilities.get_all_products_prices_links(
                                                                         html)
        html_file.close()
        #for k in prices_links_dict1.keys():
        #    print k+"\n"
        #read file2
        html_file = open(page2,'rt')
        html = html_file.read()        
        prices_links_dict2 = price_utilities.get_all_products_prices_links(
                                                                         html)        
        html_file.close()
        print('size:'+str(len(prices_links_dict2)))
        
        diffLinks = 0
        showHigher = 0
        showLower = 0
        for i in range(len(prices_links_dict1)):
            link=prices_links_dict1.keys()[i].split('@_@')[0]
            price = prices_links_dict1.values()[i]

            link2=prices_links_dict2.keys()[i].split('@_@')[0]
            price2 = prices_links_dict2.values()[i]
            
            if  link!= link2:
                diffLinks = diffLinks + 1
                if price>price2:
                    print 'more expensive product showed first' ,
                    print ("Position:"+str(i+1))
                    print price - price2
                    showHigher = showHigher +1
                else:
                    print 'less expensive product showed first',
                    showLower = showLower +1
                    print ("Position:"+str(i+1))
                    print price2 - price
                    #to fix: check something more about the product (may be from the text), do something smart :) with the price
                    #please check if in any paper they measured the price differences and how.
        print diffLinks,showHigher, showLower
        return diffLinks, showHigher,showLower
        
###########how to use################
def main_test():
    f = 'mericomanfrin@lab.imtlucca.it/mericomanfrin@lab.imtlucca.it.concord watch.shopping_testing.0.html'
    f3 = 'mericomanfrin@lab.imtlucca.it/to_delete.html'
    #links = Measurements.get_all_links(f)
    #for l in links:
    #    print(l)
    f2 = 'mericomanfrin@lab.imtlucca.it/nologin.concord watch.shopping_testing.0.html'
#    i,j = Measurements.compare_pages(f,f2)
    #(i,j,inter,inter2) = Measurements.compare_pages_links_prices(f,f2)
    #(inter,inter2) #check if aligned and equal size
    #diff = Measurements.compare_pages_mismatch(f,f2)
    #print diff
    
    x = Measurements.ncdg(f3,[f3,f3])
    print "ndcg",x
    #Measurements.ncdg()
    x,y = Measurements.editdist_and_kendalltau(f3,f3)
    print "Edit + kendall:",x, y
    print "Edit and jaccard:",Measurements.compare_pages(f3,f3)
    

def read_text_file(fileName):
    """
    Read the file and get list of testing file\n
    I must manually create the file, in this format
    xxxxx
    """
    f = open(fileName,'rt')
    
    f.close()    

def simple_analyse():    
    lux1 = [#'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.men watches.shopping_testing.0.html',
            #'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.men shoes.shopping_testing.0.html',
            #'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.car.shopping_testing.1.html',
            'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.men watches.shopping_testing.1.html',
            'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.men shoes.shopping_testing.1.html',
            'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.car.shopping_testing.2.html'
            ]    
    control_lux1 = [
        #'MarinoBellucci@lab.imtlucca.it/test/nologin.men watches.shopping_testing.0.html',
        #'MarinoBellucci@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.0.html',
        #'MarinoBellucci@lab.imtlucca.it/test/nologin.car.shopping_testing.1.html',
        'MarinoBellucci@lab.imtlucca.it/test/nologin.men watches.shopping_testing.1.html',
        'MarinoBellucci@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.1.html',
        'MarinoBellucci@lab.imtlucca.it/test/nologin.car.shopping_testing.2.html'        
    ]
    
    budget1 = [#'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.men watches.shopping_testing.0.html',
               #'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.men shoes.shopping_testing.0.html',
               #'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.car.shopping_testing.1.html',
               'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.men watches.shopping_testing.1.html',
               'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.men shoes.shopping_testing.1.html',
               'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.car.shopping_testing.2.html'
               ]
    control_budget1 = [
        'CorneliaFolliero@lab.imtlucca.it/test/nologin.men watches.shopping_testing.0.html',
        'CorneliaFolliero@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.0.html',
        'CorneliaFolliero@lab.imtlucca.it/test/nologin.car.shopping_testing.1.html',
        'CorneliaFolliero@lab.imtlucca.it/test/nologin.men watches.shopping_testing.1.html',
        'CorneliaFolliero@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.1.html',
        'CorneliaFolliero@lab.imtlucca.it/test/nologin.car.shopping_testing.2.html'        
    ]
    
    
    
    budget2 = [#'GeronimaEsposito@lab.imtlucca.it/test/GeronimaEsposito@lab.imtlucca.it.men watches.shopping_testing.0.html',
               #'GeronimaEsposito@lab.imtlucca.it/test/GeronimaEsposito@lab.imtlucca.it.men shoes.shopping_testing.0.html',
               #'GeronimaEsposito@lab.imtlucca.it/test/GeronimaEsposito@lab.imtlucca.it.car.shopping_testing.0.html',
               'GeronimaEsposito@lab.imtlucca.it/test/GeronimaEsposito@lab.imtlucca.it.men watches.shopping_testing.1.html',
               'GeronimaEsposito@lab.imtlucca.it/test/GeronimaEsposito@lab.imtlucca.it.men shoes.shopping_testing.1.html',
               'GeronimaEsposito@lab.imtlucca.it/test/GeronimaEsposito@lab.imtlucca.it.car.shopping_testing.1.html'
               ]
    control_budget2=[#'GeronimaEsposito@lab.imtlucca.it/test/nologin.men watches.shopping_testing.0.html',
                     #'GeronimaEsposito@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.0.html',
                     #'GeronimaEsposito@lab.imtlucca.it/test/nologin.car.shopping_testing.0.html',
                     'GeronimaEsposito@lab.imtlucca.it/test/nologin.men watches.shopping_testing.1.html',
                     'GeronimaEsposito@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.1.html',
                     'GeronimaEsposito@lab.imtlucca.it/test/nologin.car.shopping_testing.1.html'
                     ]
    lux2 = [#'ArnaldoFiorentino@lab.imtlucca.it/test/ArnaldoFiorentino@lab.imtlucca.it.men watches.shopping_testing.0.html',
            #'ArnaldoFiorentino@lab.imtlucca.it/test/ArnaldoFiorentino@lab.imtlucca.it.men shoes.shopping_testing.0.html',
            #'ArnaldoFiorentino@lab.imtlucca.it/test/ArnaldoFiorentino@lab.imtlucca.it.car.shopping_testing.0.html',
            'ArnaldoFiorentino@lab.imtlucca.it/test/ArnaldoFiorentino@lab.imtlucca.it.men watches.shopping_testing.1.html',
            'ArnaldoFiorentino@lab.imtlucca.it/test/ArnaldoFiorentino@lab.imtlucca.it.men shoes.shopping_testing.1.html',
            'ArnaldoFiorentino@lab.imtlucca.it/test/ArnaldoFiorentino@lab.imtlucca.it.car.shopping_testing.1.html'
            ]    
    control_lux2= [#'ArnaldoFiorentino@lab.imtlucca.it/test/nologin.men watches.shopping_testing.0.html',
                   # 'ArnaldoFiorentino@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.0.html',
                    #'ArnaldoFiorentino@lab.imtlucca.it/test/nologin.car.shopping_testing.0.html',
                    'ArnaldoFiorentino@lab.imtlucca.it/test/nologin.men watches.shopping_testing.1.html',
                    'ArnaldoFiorentino@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.1.html',
                    'ArnaldoFiorentino@lab.imtlucca.it/test/nologin.car.shopping_testing.1.html'
                    ]
    
    
    ##################################################THIS PARTH is separated############################
    ## for group of 2 accounts but after many many training before, to see how it is now
    lux11 = ['MarinoBellucci@lab.imtlucca.it/test2/MarinoBellucci@lab.imtlucca.it.men watches.shopping_testing.0.html',
            'MarinoBellucci@lab.imtlucca.it/test2/MarinoBellucci@lab.imtlucca.it.gold watches.shopping_testing.0.html',
            'MarinoBellucci@lab.imtlucca.it/test2/MarinoBellucci@lab.imtlucca.it.men shoes.shopping_testing.0.html',
            'MarinoBellucci@lab.imtlucca.it/test2/MarinoBellucci@lab.imtlucca.it.car.shopping_testing.0.html'#,
            #'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.men watches.shopping_testing.1.html',
            #'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.men shoes.shopping_testing.1.html',
            #'MarinoBellucci@lab.imtlucca.it/test/MarinoBellucci@lab.imtlucca.it.car.shopping_testing.2.html'
            ]    
    control_lux11 = [
        'MarinoBellucci@lab.imtlucca.it/test2/nologin.men watches.shopping_testing.0.html',
        'MarinoBellucci@lab.imtlucca.it/test2/nologin.gold watches.shopping_testing.0.html',
        'MarinoBellucci@lab.imtlucca.it/test2/nologin.men shoes.shopping_testing.0.html',
        'MarinoBellucci@lab.imtlucca.it/test2/nologin.car.shopping_testing.0.html'#,
        #'MarinoBellucci@lab.imtlucca.it/test2/nologin.men watches.shopping_testing.1.html',
        #'MarinoBellucci@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.1.html',
        #'MarinoBellucci@lab.imtlucca.it/test/nologin.car.shopping_testing.2.html'        
    ]
    
    budget11 = ['CorneliaFolliero@lab.imtlucca.it/test2/CorneliaFolliero@lab.imtlucca.it.men watches.shopping_testing.0.html',
                'CorneliaFolliero@lab.imtlucca.it/test2/CorneliaFolliero@lab.imtlucca.it.gold watches.shopping_testing.0.html',
               'CorneliaFolliero@lab.imtlucca.it/test2/CorneliaFolliero@lab.imtlucca.it.men shoes.shopping_testing.0.html',
               'CorneliaFolliero@lab.imtlucca.it/test2/CorneliaFolliero@lab.imtlucca.it.car.shopping_testing.0.html'#,
               #'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.men watches.shopping_testing.1.html',
               #'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.men shoes.shopping_testing.1.html',
               #'CorneliaFolliero@lab.imtlucca.it/test/CorneliaFolliero@lab.imtlucca.it.car.shopping_testing.2.html'
               ]
    control_budget11 = [
        'CorneliaFolliero@lab.imtlucca.it/test2/nologin.men watches.shopping_testing.0.html',
        'CorneliaFolliero@lab.imtlucca.it/test2/nologin.gold watches.shopping_	testing.0.html',
        'CorneliaFolliero@lab.imtlucca.it/test2/nologin.men shoes.shopping_testing.0.html',
        'CorneliaFolliero@lab.imtlucca.it/test2/nologin.car.shopping_testing.0.html'#,
        #'CorneliaFolliero@lab.imtlucca.it/test/nologin.men watches.shopping_testing.1.html',
        #'CorneliaFolliero@lab.imtlucca.it/test/nologin.men shoes.shopping_testing.1.html',
        #'CorneliaFolliero@lab.imtlucca.it/test/nologin.car.shopping_testing.2.html'        
    ]    


    
    folder1 = 'folder1'
    folder2 = 'folder2'
    products = ['men watches','men shoes','car']
    print 'calculate ndcg'
    for i in range(len(lux2)):
        
        #regard to only the group2:new training
        print('for product '+ products[i])
        print('>luxury=\t\t'+str(Measurements.ncdg(lux2[i],[lux2[i],budget2[i],control_lux2[i],control_budget2[i]])))
        print Measurements.compare_pages(lux2[i],budget2[i])
        
        print('>control luxury=\t'+str(Measurements.ncdg(control_lux2[i],[lux2[i],budget2[i],control_lux2[i],control_budget2[i]])))
        
        print('>budget=\t\t'+str(Measurements.ncdg(budget2[i],[lux2[i],budget2[i],control_lux2[i],control_budget2[i]])))
        
        print('>control budget=\t'+str(Measurements.ncdg(control_budget2[i],[lux2[i],budget2[i],control_lux2[i],control_budget2[i]])))    
        
        print("======================================")               
        
                
        
    print("#####################################")    
    print('this is for only group of old training accounts')
    #only for group old training
    for i in range(len(lux11)):
        print('for product '+ str(i))
        print('>luxury=\t\t'+str(Measurements.ncdg(lux11[i],[lux11[i],budget11[i],control_lux11[i],control_budget11[i]])))
        
        print('>control luxury=\t'+str(Measurements.ncdg(control_lux11[i],[lux11[i],budget11[i],control_lux11[i],control_budget11[i]])))
        
        print('>budget=\t\t'+str(Measurements.ncdg(budget11[i],[lux11[i],budget11[i],control_lux11[i],control_budget11[i]])))
        
        print('>control budget=\t'+str(Measurements.ncdg(control_budget11[i],[lux11[i],budget11[i],control_lux11[i],control_budget11[i]])))    
        
        print("======================================")        
        
    
        
    
    
#if __name__ == '__main__':
    #simple_analyse()
    
    #budget
    #0.819558885708 -->0.785086948479
    #0.836496922672 -->0.910459171526
    #0.775378068366 -->0.711397432038
    
    
    
    #lux
    #0.797746013391->0.791524210967
    #0.820407632288->0.905447057427
    #0.708171412734->0.775252219645

    
    
    ##########
    ########
    # buoc 1: tao danh sach file name, chi co 1 it file ma thoi
    # buoc 2: run the code
import os
from collections import OrderedDict, defaultdict
    
def preparation():
    ECO = 'eco'
    LUX = 'lux'
    NONE = 'none'
    list_of_testing =[
    "mens dress casual shoes",
    "luxury shoe",
    "dance boot",
    "comfortable shoes",
    "womens trendy boots",
    "luxury jean",
    "casual jean" ]
    list_of_accounts = OrderedDict( {
        "BaccoTrevisani@lab.imtlucca.it":ECO,
        "AlviseBergamaschi@lab.imtlucca.it":LUX,
        "no_email71":NONE,
        "no_email81":NONE,
        "CrispinaMoretti@lab.imtlucca.it":ECO,
        "LeliaGenovesi@lab.imtlucca.it":LUX,
        "no_email51":NONE,
        "no_email61":NONE   
    })
    
    
    folder_path = '/home/vino/AdFisher_Code/examples/experiment_01_ny7_8_shoes/'
    'CorneliaFolliero@lab.imtlucca.it'
    'CorneliaFolliero@lab.imtlucca.it/test2/CorneliaFolliero@lab.imtlucca.it.car.shopping_testing.0.html'#,
    # folder/email.keyword.shopping_testing.{i}
    a = []  
    ndcg_dict = defaultdict(list)  
    for i in range(10): # each round
        for keyword in list_of_testing: # each keywords
            keyword = "casual jean"
            
            list_file = []
            for email in list_of_accounts.keys(): # each account
                #print(folder_path + email + '.' + keyword + '.' + 'shopping_testing.' + str(i) + ".html")
                if os.path.isfile(folder_path + email + '.' + keyword + '.' + 'shopping_testing.' + str(i) + ".html"):
                    list_file.append(folder_path + email + '.' + keyword + '.' + 'shopping_testing.' + str(i) + ".html")
            #calculate the ndcg after each keywords
            print('Keywords for round ', str(i) + ": " + keyword)         
            for file_ in list_file: # each account again
                try:
                    nd = Measurements.ncdg(file_,[file2 for file2 in list_file])
                    print( "{}\t{}").format( nd,file_.split('/')[-1].split('.')[0])
                    ndcg_dict[file_.split('/')[-1].split('.')[0]].append(nd)                    
                except Exception as e:
                    print(e)
            #print(ndcg_dict)                    
            break
    print(ndcg_dict)            
    #BaccoTrevisani@lab.imtlucca.it.mens dress casual shoes.shopping_testing.0.html
    #BaccoTrevisani@lab.imtlucca.it.mens dress casual shoes.shopping_testing.0.html
    domain = "@lab.imtlucca.it"
    
    print('=======finish===========')
    
    
if __name__ == '__main__':
    preparation()
    
