# -*- coding: utf-8 -*-
import getpass

from scrapy.http import Request, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders.init import InitSpider


class FourClojureSpider(CrawlSpider):
    name = '4clojure'

    allowed_domains = ['4clojure.com']
    start_urls = ['http://www.4clojure.com/problems']
    problem_seed = r'/problem/\d+$'

    rules = (
        Rule(LinkExtractor(allow=problem_seed),
             callback='parse_problem', follow=False),
    )

    def parse_problem(self, response):
        yield {
            'number': response.css('div#prob-number::text').extract_first(),
            'title': response.css('div#prob-title::text').extract_first(),
            'difficulty': response.css("table#tags td:contains('Difficulty:') + td::text").extract_first(),
            'cases': [c.strip() for c in response.css('table.testcases tr').xpath('.//text()').extract()],
            'solution': response.css('textarea#code-box::text').extract_first(),
        }


class FourClojureWithLogin(InitSpider, FourClojureSpider):
    name = '4clojure-login'

    login_page = 'http://www.4clojure.com/login'

    def init_request(self):
        return Request(url=self.login_page, callback=self.login, dont_filter=True)

    def login(self, response):
        return FormRequest.from_response(
            response,
            formdata={'user': input('Username: '), 'pwd': getpass.getpass('Password: ')},
            callback=self.check_login_response
        )

    def check_login_response(self, response):
        if "Logged in as" in response.text:
            self.log("Login succeeded.")
            return self.initialized()
        else:
            self.log("Login failed.")