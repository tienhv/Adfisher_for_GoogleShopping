import logging

from scipy.stats import kendalltau
class Measurements():
    """
    Calculates edit distance and jaccard distance
    get all links
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)
    is_from_file = True
    @staticmethod
    def get_all_links(file1):
        """Return a list of links extracted from file1
        file1: full path to file, type:string, i.e, '/root/name.txt'
        get all links from the file1
        Args:
            - file1: full path to file contains all link in text, each line is one datum
            - not_file: True: this is a file
                        False: file1 is a list, so easy now, no need to read
        """
        links = []
        #Measurements.logger.critical("Value of is_from_file is %s", str(Measurements.is_from_file))
        if Measurements.is_from_file is True:
            with open(file1) as f:
                #if the file is valid:, store it
                for line in f:
                    if line:
                        links.append(line)
        else:
            links = file1 # file1 is alrealy a list of data
        # do processing here
        return links

    @staticmethod
    def pages_to_alphabet(pages):
        """Convert links to alphabet
        pages: is a list of file name (full path)
        Example: ['/root/a.txt','/root/b.txt']
        """
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
        """Convert a list of links to a set of links, nothing changed in data
        """
        #s = set()
        links = Measurements.get_all_links(page)
        s = set(links)
        return s

    @staticmethod
    def page_to_string(page, alph):
        """convert a list of link inside file to a string
            page: full path to file .i.e, '/root/a.txt'
            alph: return of pages_to_alphabet
        """
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
        #Measurements.logger.debug("From page1:",page1)
        str1 = Measurements.page_to_string(page1, alph)
        #Measurements.logger.debug("From page2:"+page2)
        str2 = Measurements.page_to_string(page2, alph)
        # so sanh coi cai nay giong cai kia bao nhieu phan tram
        if len(s1) > len(s2):
            j = float(len(s1.intersection(s2)))/len(s1)
        else:
            j = float(len(s2.intersection(s1)))/len(s2)
        return j


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
        j, e = Measurements.compare_pages(page1, page2)
        return (j, e, kendalltau(l1, l2)[0])

    @staticmethod
    def calucate_kendall(page1, page2, from_file = True):
        Measurements.is_from_file = from_file
        alph = Measurements.pages_to_alphabet([page1, page2])
        str1 = Measurements.page_to_string(page1, alph)
        str2 = Measurements.page_to_string(page2, alph)
        str1 = unicode(str1, 'utf-8',errors='ignore')
        str2 = unicode(str2, 'utf-8',errors='ignore')
        l1 = [a for a in str1]
        l2 = [a for a in str2]
        while len(l1) < len(l2): l1.append('null')
        while len(l2) < len(l1): l2.append('null')
        return kendalltau(l1, l2)[0]

    @staticmethod
    def calculate_jaccard(page1, page2, from_file = True):
        Measurements.is_from_file = from_file
        j = Measurements.compare_pages(page1, page2)
        return j#,e

    @staticmethod
    def calculate_jaccard_kendall(page1, page2, from_file = True):
        """ calculate jaccard and kendall from two files. Return a tuple(jaccard, kendall), float number.
        page1, page2: full path to two files
        """
        Measurements.is_from_file = from_file
        
        alph = Measurements.pages_to_alphabet([page1, page2])
        str1 = Measurements.page_to_string(page1, alph)
        str2 = Measurements.page_to_string(page2, alph)
        str1 = unicode(str1, 'utf-8',errors='ignore')
        str2 = unicode(str2, 'utf-8',errors='ignore')
        l1 = [a for a in str1]
        l2 = [a for a in str2]
        while len(l1) < len(l2): l1.append('null')
        while len(l2) < len(l1): l2.append('null')
        #-----
        s1 = Measurements.link_to_set(page1)
        s2 = Measurements.link_to_set(page2)
        j = 0 # this is jaccard
        if len(s1) > len(s2):
            j = float(len(s1.intersection(s2)))/len(s1)
        else:
            j = float(len(s2.intersection(s1)))/len(s2)
        #-----
        k = kendalltau(l1, l2)[0]
        return j, k

    #TODO how to calculate unlimited number of files instead of 2
###########how to use################o

def main_test():
    #modify the get_all_links as your needs
    #print 'Jaccard index:', Measurements.calculate_jaccard('b.txt','a.txt')
    #print 'Kendall:', Measurements.calucate_kendall('a.txt','b.txt')
    Measurements.is_from_file = True
    Measurements.get_all_links('a')
    #print 'K&J:', Measurements.calculate_jaccard_kendall('a.txt','b.txt')


if __name__ == "__main__":
    main_test()

