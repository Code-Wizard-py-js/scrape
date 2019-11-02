import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from dateutil import parser
from datetime import datetime,timedelta
from pyvirtualdisplay import Display
class Scrap_Zomato:
    '''Scrap Zomato'''

    def __init__(self,link):
        self.link=link

    def open_driver_with_headless(self,url):
        '''
        open driver
        '''
        display = Display(visible=0, size=(800, 800))  
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
        browser = webdriver.Chrome(excutable_path=r"/home/mrmr5669/chromedriver", chrome_options=chrome_options )  
                
        browser.get(url)
        return browser

    def open_driver(self,url):
        '''
        open driver
        '''
       
        browser = webdriver.Chrome(executable_path=r'/home/mrmr5669/chromedriver')
        browser.get(url)
        return browser

    def get_soup(self,browser):
        '''
        fetch the html part of current browser
        '''
        html = browser.page_source
        return BeautifulSoup(html,"html.parser")

    def get_html(self,article):
        '''get all the details'''
        
       
        dic={}        
        reviewer_detail={}

        name_value=article.find('div',{'class':'header nowrap ui left'})
        reviewer_detail['name']=name_value.text.strip() if name_value else ''
        reviewer_detail['reviewer_profile']=name_value.find('a')['href'] if name_value else ''
        dic['reviewer']=reviewer_detail

        dic['extra_data']={}
        
        dataval=article.find('div',{'class':'rev-text mbot0'})
        data_value=dataval.text if dataval else ''
        dic['description']=data_value.split('\n')[2].strip() if data_value else ''

        try:
            dic['rating']=int(article.find('div',{'class':'tooltip'})['aria-label'].split()[1][0])
        except:
            dic['rating']=0
        
        dic['heading']=''
        dic['smiley_value']=''
        dic['review_type']='STAR'
        dateval=article.find('time').text if article.find('time') else ''
        if dateval:
            try:               
                dic['review_create']=parser.parse(dateval)
            except:
                if dateval=='yesterday':
                    dateans=1
                else:
                    dateval=dateval.split()
                    if dateval[0]=='one':
                        dateval[0]=1
                    
                    tt=dateval[1]
                    if tt=='years':
                        dateans=int(dateval[0])*365
                    elif tt=='year':
                        dateans=365
                    elif tt=='weeks':
                        dateans=int(dateval[0])*7
                    elif tt=='week':
                        dateans=7
                    elif tt=='months':
                        dateans=int(dateval[0])*30
                    elif tt=='month':
                        dateans=30
                    elif tt=='days':
                        dateans=int(dateval[0])
                    elif tt=='day':
                        dateans=1                
                    elif tt=='minutes' or tt=='minute' or tt=='second'or tt=='hour' or tt=='seconds' or tt=='hours' :
                        dateans=0
                dic['review_create']=datetime.now()-timedelta(days=dateans)

        dic['is_thum_up']=False
        dic['status']='NOT_RESPONDED'

        print(dic)
       
        return dic

    def scrapper(self,**kwargs):
        
        data=[] # contain all reviews in list of dictionary form
        page_no=1 
        old_len=0
        url=self.link.split('?')[0]
        if url.endswith=='/reviews':
            browser=self.open_driver(url)
        else:
            browser=self.open_driver(url+'/reviews')
            
        time.sleep(2)
        try:
            '''click all reviews button'''
            browser.find_element_by_xpath("//a[contains(text(),'All Reviews')]").click()
            time.sleep(5)
        except:
            #logger.info("all_reviews button not found or it has default all_reviews button")
            pass

        soup=self.get_soup(browser)
        page_per_count=0
             
        while True:  
            try:
                '''close the popup'''
                browser.find_element_by_class_name('close icon').click()
                time.sleep(2)
                #logger.info("popup box exist")
            except:
                pass

            print("page no",page_no)

            '''get all the reviews''' 
            all_articles=soup.find_all('div',{'class':'stupendousact'})
            new_len=len(all_articles)
            page_per_count=(new_len-old_len) if (new_len-old_len)>page_per_count else page_per_count
            dic=self.get_html(all_articles[old_len])

            """'''match the first review on every page in database '''
            dic.pop('review_create')
            '''match all the keys except Review_create'''
            if Review.objects.filter(branch=self.link_instance.branch,**dic).exists():
                all_articles=all_articles[:old_len]
                break"""

            '''check if the load more button exists or not'''
            load_button=soup.find_all('span',{'class':'zs-load-more-count'})
            if new_len==old_len or len(load_button)==0:
                print("total reviews",len(all_articles))
                break
            '''click the load more button'''
            browser.find_element_by_class_name('zs-load-more-count').click()
            time.sleep(15)
            soup=self.get_soup(browser)
            
            old_len=new_len
            page_no+=1
        
        for article in all_articles:
            data.append(self.get_html(article))
        
        browser.close()
        
        return data,page_per_count

Scrap_Zomato('https://www.zomato.com/mumbai/veranda-pali-hill-bandra-west?zrp_bid=18357374').scrapper()
    


