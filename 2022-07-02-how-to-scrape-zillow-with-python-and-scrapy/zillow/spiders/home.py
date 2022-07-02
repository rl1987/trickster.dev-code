import scrapy
from scrapy.http import JsonRequest

from urllib.parse import urlparse, parse_qs, urlencode, urljoin
import json

import js2xml

from zillow.items import Property

class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['zillow.com']
    start_urls = [ 'https://www.zillow.com/homes/NY_rb/' ]
    request_id = 1

    def __init__(self, start_urls=None):
        super().__init__()

        if start_urls is not None:
            self.start_urls = start_urls.split('|')

    def start_requests(self):
        fsbo_url = 'https://www.zillow.com/homes/fsbo/'

        yield scrapy.Request(fsbo_url, callback=self.start_main_requests)

    def start_main_requests(self, response):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.parse_property_list_html)

    def generate_api_url_from_search_query_state(self, search_query_state_json_str):
        wants = {
            'cat1' : ['total'],
            'cat2' : ['listResults']
        }

        wants_json_str = json.dumps(wants)

        new_params = {
                'searchQueryState' : search_query_state_json_str,
                'wants' : wants_json_str,
                'requestId' : self.request_id,
        }

        api_url = 'https://www.zillow.com/search/GetSearchPageState.htm?' + urlencode(new_params)

        self.request_id += 1

        return api_url

    def parse_property_list_html(self, response):
        js = response.xpath('//script[contains(text(), "searchQueryState")]/text()').get()

        if js is not None:
            parsed = js2xml.parse(js)

            search_state_url = parsed.xpath('//string[contains(text(), "searchQueryState")]/text()')[0]

            params = parse_qs(o.query)

            search_query_state_json_str = params['searchQueryState'][0]
        else:
            json_str = response.xpath('//script[@data-zrr-shared-data-key="mobileSearchPageStore"]/text()').get()
            if json_str is None:
                self.logger.error("Failed to find search query state")
                return

            json_str = json_str.replace('<!--', '').replace('-->', '')

            json_dict = json.loads(json_str)
            
            search_query_state = json_dict.get('queryState')

            search_query_state_json_str = json.dumps(search_query_state)
    
        api_url = self.generate_api_url_from_search_query_state(search_query_state_json_str)

        yield scrapy.Request(api_url, callback=self.parse_property_list_json)

    def parse_property_list_json(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        search_results = json_dict.get('cat2', dict()).get('searchResults', dict()).get('listResults', [])

        for result in search_results:
            zpid = result.get('zpid')
            query_id = '4c19ac196fd0f1e7e30ca7e7f9af85d5'
            operation_name = 'ForSaleDoubleScrollFullRenderQuery'

            url_params = {
                'zpid': zpid,
                'contactFormRenderParameter': '',
                'queryId': query_id,
                'operationName': operation_name,
            }
            
            json_payload = {
                'clientVersion' : "home-details/6.0.11.5970.master.8d248cb",
                'operationName' : operation_name,
                'queryId' : query_id,
                'variables' : {
                    'contactFormRenderParameter' : {
                        'isDoubleScroll' : True,
                        'platform' : 'desktop',
                        'zpid' : zpid,
                    },
                    'zpid' : zpid
                }
            }

            api_url = 'https://www.zillow.com/graphql/?' + urlencode(url_params)

            yield JsonRequest(url=api_url, data=json_payload, callback=self.parse_property_page_json)

        next_url = json_dict.get('cat2', dict()).get('searchList', dict()).get('pagination', dict()).get('nextUrl')
        
        if next_url is not None:
            o = urlparse(response.url)
            old_params = parse_qs(o.query)

            old_search_query_state_json_str = old_params['searchQueryState'][0]

            search_query_state = json.loads(old_search_query_state_json_str)

            if search_query_state.get('pagination') is None:
                search_query_state['pagination'] = {'currentPage': 2}
            else:
                search_query_state['pagination']['currentPage'] += 1

            search_query_state_json_str = json.dumps(search_query_state)

            api_url = self.generate_api_url_from_search_query_state(search_query_state_json_str)

            yield scrapy.Request(api_url, callback=self.parse_property_list_json)

    def parse_property_page_json(self, response):
        json_dict = json.loads(response.text)
        data_dict = json_dict.get('data', dict())
        property_dict = data_dict.get('property')
        if property_dict is None:
            return

        item = Property()
    
        item['url'] = property_dict.get('hdpUrl')
        if item.get('url') is not None:
            item['url'] = urljoin(response.url, item['url'])

        item['address'] = property_dict.get('streetAddress')
        item['city'] = property_dict.get('address', dict()).get('city')
        item['state'] = property_dict.get('address', dict()).get('state')
        item['zipcode'] = property_dict.get('address', dict()).get('zipcode')
        item['price'] = property_dict.get('price')
        item['zestimate'] = property_dict.get('zestimate')
        item['n_bedrooms'] = property_dict.get('bedrooms')
        item['n_bathrooms'] = property_dict.get('bathrooms')
        item['area'] = property_dict.get('livingArea')
        item['latitude'] = property_dict.get('latitude')
        item['longitude'] = property_dict.get('longitude')
        
        contact_data_dict = property_dict.get('contactFormRenderData', dict()).get('data', dict())
        agent_module = contact_data_dict.get('agent_module')
        if agent_module is not None:
            phone_dict = agent_module.get('phone')
            if phone_dict is not None:
                item['phone'] = "({}) {}-{}".format(phone_dict.get('areacode'), phone_dict.get('prefix'), phone_dict.get('number'))
 
        huge_photos = property_dict.get('hugePhotos')
        if huge_photos is not None:
            item['image_urls'] = list(map(lambda img: img.get('url'), huge_photos))

        yield item

