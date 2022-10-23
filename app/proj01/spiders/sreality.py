import scrapy
import psycopg2
import logging


from scrapy.exceptions import CloseSpider

from proj01.items import Proj01Item
from scrapy_playwright.page import PageMethod

# from scrapy.utils.response import open_in_browser


class SrealitySpider(scrapy.Spider):
    name = 'sreality'

    yieldCounter = 0
    yieldResult = []

    custom_settings = {'FEED_EXPORT_ENCODING': 'UTF-8'}

    def start_requests(self):
        yield scrapy.Request('https://www.sreality.cz/hledani/prodej/byty',
                             meta=dict(
                                 playwright=True,
                                 playwright_page_methods=[PageMethod('wait_for_selector', 'div.paging')]
                             ), callback=self.parse)

    def parse(self, response):

        # open_in_browser(response)

        nextpageurl = response.css("a.paging-next::attr(href)")

        yield from self.scrape(response)

        if nextpageurl:
            path = nextpageurl.extract_first()
            nextpage = response.urljoin(path)
            print("Found url: {}".format(nextpage))
            yield scrapy.Request(nextpage, meta=dict(
                playwright=True,
                playwright_page_methods=[PageMethod('wait_for_selector', 'div.paging')]
            ), callback=self.parse)
        else:
            print("ERR NEXT PAGE NOT FOUND")

    def scrape(self, response):

        for resource in response.css('.property'):
            if self.yieldCounter < 500:
                # Loop over each item on the page.
                item = Proj01Item()  # Creating a new Item object

                item['description'] = resource.css('.name::text').get()
                item['image'] = resource.css('img::attr(src)').get()

                self.yieldCounter += 1
                self.yieldResult.append(item)
                yield item
            else:
                self.write_to_db()
                raise CloseSpider('scraped_enough')

    def write_to_db(self):
        conn = psycopg2.connect(
            host="db",
            database="srealitydb",
            user="postgres",
            password="root")

        cursor = conn.cursor()

        # cursor.execute("CREATE TABLE public.properties (id integer NOT NULL, title character varying, image character varying);ALTER TABLE public.properties OWNER TO postgres;CREATE SEQUENCE public.properties_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1; ALTER TABLE public.properties_id_seq OWNER TO postgres; ALTER SEQUENCE public.properties_id_seq OWNED BY public.properties.id; ALTER TABLE ONLY public.properties ALTER COLUMN id SET DEFAULT nextval('public.properties_id_seq'::regclass); ALTER TABLE ONLY public.properties ADD CONSTRAINT properties_pkey PRIMARY KEY (id);")
        # conn.commit()

        for result in self.yieldResult:
            cursor.execute("INSERT INTO properties(title, image) VALUES(%s, %s)",
                           (result['description'], result['image']))

        logging.warning("DBGM1")
        conn.commit()
        logging.warning("DBGM2")
        cursor.close()
        logging.warning("DBGM3")
        conn.close()
        logging.warning("DBGM4")





