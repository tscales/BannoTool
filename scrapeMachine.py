import requests, re
from bs4 import BeautifulSoup
from collections import Counter

class BannoScrapeTool:
    def __init__(self):
        self.HOMEURL = 'https://www.banno.com'
        self.PRODUCTURL = 'https://www.banno.com/features'
        self.response = requests.get(self.HOMEURL)
        self.check_status_code(self.response.status_code)
        self.html = BeautifulSoup(self.response.text, "html.parser")
        print('''
        ##############
        #            #
        # BANNO TOOL #
        #            #
        ##############

        '''
        )

    def get_products_offered(self):
        """Generates a list of all divs including the class
        'feature-group-label'
        and returns the list length
        """
        self.products_response = requests.get(self.PRODUCTURL)
        self.check_status_code(self.products_response.status_code)
        self.products_html = BeautifulSoup(self.products_response.text, "html.parser")
        self.products_list = self.products_html.find_all("div",{"class": "feature-group-label"})

        return "Number of products offered: " + str(len(self.products_list)) + '\n'


    def get_top_chars(self):
        """ finds the top three alphanumeric characters
        the Counter function acts as a hash table where the element is the key
        and the count is the value
        """
        self.alphanum_str = re.sub(r'\W+','',self.html.text)
        ret_str = 'Three most common alphanumeric characters:\n'
        self.count_res = Counter(self.alphanum_str.lower())
        for c in self.count_res.most_common(3):
            ret_str += c[0] + ': ' + str(c[1]) + '\n'
        return ret_str

    def get_png_count(self):
        """counts the number of IMG tags and
        filters out non PNG images
        to find all instances of .png(meta tags, srcsets): use re.findall('.png',self.response.text)
        """
        return "Number of png images: " + str(len([img for img in self.html('img') if img['src'][-3:]=='png'])) + '\n'

    def get_twitter_handle(self):
        """return banno twitter handle"""
        return "Banno Twitter Handle: " + str(self.html.find("meta",{"name":"twitter:site"})['content']) + '\n'

    def get_FI_count(self):
        """find all instances of financial instituion
        (including plurals of institution)"""
        return "'financial institution' occurs " + str(len(re.findall('financial institution',self.response.text))) + " times." + '\n'

    def check_status_code(self,status_code):
        if status_code == 200:
            return
        else:
            raise exception("expected status code 200, got " + str(status_code))
