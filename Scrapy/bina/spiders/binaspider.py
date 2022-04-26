import scrapy
import pickle

class BinaspiderSpider(scrapy.Spider):


    """There are not phone numbers because time limitations"""
    name = 'binaspider'
    allowed_domains = ['https://bina.az/']
    start_urls = ['https://bina.az/']

    link_elements=pickle.load(open('announcement_links.pkl','rb'))


    def parse(self,response):
        for link in BinaspiderSpider.link_elements:
            yield scrapy.Request(link, callback=self.parse_annoucements,dont_filter=True)

    def parse_annoucements(self, response):

        table=response.css('table.parameters  tr td::text').getall()
        table=dict(zip(table[::2], table[1::2]))

        agency_name=response.css('h1.agency--title::text').get()
        if agency_name:
            table['Agency Name']=agency_name

        table['Price']=response.css('span.price-val::text').get().replace(" ","")
        table['Currency']=response.css('span.price-cur::text').get()
        table['Unit Price']=response.css('div.unit-price::text').get()
        
        
        table['Description']="".join(response.xpath('//article//text()').getall())
        #Map And Locations
        table['Adress']=response.css('div.map_address::text').get()
        table['Locations']=response.css('ul.locations li a::text').getall()
        
        table['Latitute']=response.css('div#item_map').xpath('@data-lat').get()
        table['Longitude']=response.css('div#item_map').xpath('@data-lng').get()
        
        # #Seller
        table['Seller Name']=response.css('div.name::text').get()
        table['Ownership']=response.css('span.ownership::text').get()
        # table['Phone Numbers']=response.css('div.js-phones li::text').getall()
        
        # #Announce Info
        item_info=response.css('div.item_info p::text').getall()
        table['Announcement ID']=item_info[0]
        table['Views']=item_info[1]
        table['Update Time']=item_info[2]

        yield table
