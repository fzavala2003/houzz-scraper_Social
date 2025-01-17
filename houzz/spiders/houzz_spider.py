import time
from bs4 import BeautifulSoup
import scrapy
from scrapy_playwright.page import PageMethod
from playwright._impl._errors import TimeoutError

from houzz.spiders.utils import extract_emails_from_url

class HouzzSpider(scrapy.Spider):
    name = "houzz_spider"
    base_url="https://www.houzz.com"

    custom_settings = {
        'FEEDS': {
            'output.csv': {
                'format': 'csv',
                'overwrite': True,  # Set to True to overwrite the file if it already exists
            },
        }
    }

    def start_requests(self):
        houzz_interior_designers_link="https://www.houzz.com/professionals/interior-designer/carter-lake-ia-us-probr0-bo~t_11785~r_4850531"
        yield scrapy.Request(
            url=houzz_interior_designers_link,
            callback=self.parse,
            meta={
                "playwright": True, 
                "playwright_include_page": True,
                "playwright_page_methods":[PageMethod("wait_for_load_state", "load")]
            },
            errback=self.error_handler
        )

    async def parse(self, response):
        if response.status==200:
            houzz_interior_designers_page=response.meta["playwright_page"]
            houzz_interior_designers_page_html=await houzz_interior_designers_page.content()
            scp=scrapy.Selector(text=houzz_interior_designers_page_html)
            designers_url_list=scp.css("a.hz-pro-ctl::attr(href)").getall()
            for i in range(len("designers_url_list")):
                yield scrapy.Request(
                    designers_url_list[i], 
                    callback=self.parse_subpage,
                    meta={
                        "playwright": True,  
                        "playwright_include_page": True,
                        "playwright_page_methods":[PageMethod("wait_for_load_state", "load")],
                        "playwright_context": "new"+str(i+1)
                    },
                    errback=self.error_handler
                    
                )
        
        
        """ 
        next_page=scp.css("a.hz-pagination-link--next::attr(href)").get()
        if next_page:
          
            yield scrapy.Request(
                url, 
                callback=self.parse_subpage,
                meta={
                    "playwright": True,  
                    "playwright_include_page": True,
                    "playwright_page_methods":[PageMethod("wait_for_load_state", "load")],
                    "playwright_context": "new"
                }
                
            )
        """
    async def parse_subpage(self, response):
        if(response.status==200):
            designer_page=response.meta["playwright_page"]
            designers_page_html=await designer_page.content()
            soup = BeautifulSoup(designers_page_html, 'html.parser')
            data = {"url": response.url}

            business_section = soup.find('section', id='business')
        
            for div in business_section.find_all('div'):
                h3 = div.find('h3')
                if h3:
                    key = h3.get_text(strip=True)
                    p = div.find('p')
                    if p:
                        value = p.get_text()
                        data[key] = value
                        print(key, value)
                       
                        if "Find" in value:
                            network_names=value.split("Find me on ")[1:]
                            print(network_names)
                            social_networks_dic={}
                            links_containers = div.find_all('a')
                            network_links=[]
                            for link_container in links_containers:
                                network_links.append(link_container.get('href'))
                            
                            for i in range(len(network_names)):
                                social_networks_dic[network_names[i]]=network_links[i]
                            data[key]=social_networks_dic
            
            if "Website" in data:
                found_emails = extract_emails_from_url(data["Website"])
                data["Emails"] = found_emails
            
            await designer_page.close()
            yield data
    
    async def error_handler(self, failure):
        page=failure.request.meta["playwright_page"]
        await page.close()
        if isinstance(failure.value, TimeoutError):
            print("TimeoutError, url: ", failure.request.url)


    

