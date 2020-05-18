import scrapy
# scrapy crawl amazon_links -o amazon_links.json


class QuotesSpider(scrapy.Spider):
     name = "amazon_links"

     #start_urls = [
     #     'https://www.amazon.com/Laptops-Computers-Tablets/s?rh=n%3A565108&page=',
     #]

     start_urls=[]
     myBaseUrl = 'https://www.amazon.com/Laptops-Computers-Tablets/s?rh=n%3A565108&page='
     for i in range(1,3):
          start_urls.append(myBaseUrl+str(i))


     def parse(self, response):
          data = response.css("a.a-text-normal::attr(href)").getall()
          # links = [s for s in data if "links" in s] 
          links =   [s for s in data if "Lenovo-"  in  s
                                     or "LENOVO-"  in  s
                                     or "Hp-"      in  s
                                     or "HP-"      in  s
                                     or "Acer-"    in  s
                                     or "ACER-"    in  s
                                     or "Dell-"    in  s
                                     or "DELL-"    in  s
                                     or "Samsung-" in  s
                                     or "SAMSUNG-" in  s
                                     or "Asus-"    in  s
                                     or "ASUS-"    in  s
                                     or "Toshiba-" in  s
                                     or "TOSHIBA-" in  s
                                     # or "Apple-"   in  s
                                     # or "APPLE-"   in  s
                    ]

          links = list(dict.fromkeys(links))
          # links = [s for s in links if "#customerReviews" in s]
          links = [s for s in links if "#customerReviews"   not in s]
          links = [s for s in links if "#productPromotions" not in s]

          for  i in range(len(links)):
          # for  i in range(2):
               links[i] = response.urljoin(links[i])
               yield response.follow(links[i], self.parse_compDetails)


     def parse_compDetails(self, response):
          def extract_with_css(query):
               return response.css(query).get(default='').strip()

          price = response.css("#priceblock_ourprice::text").get()


          product_details_table  = response.css("#productDetails_detailBullets_sections1")
          product_details_values = product_details_table.css("td.a-size-base::text").getall()
          k = []
          for i in product_details_values:
               i = i.strip()
               k.append(i)
          product_details_values = k

          ASIN = product_details_values[0]

          average_customer_reviews = product_details_values[4]

          number_reviews_div = response.css("#reviews-medley-footer")
          number_reviews_ratings_str  = number_reviews_div.css("div.a-box-inner::text").get()
          number_reviews_ratings_str  = number_reviews_ratings_str.replace(',', '')
          number_reviews_ratings_str  = number_reviews_ratings_str.replace('.', '')
          number_reviews_ratings_list = [int(s) for s in number_reviews_ratings_str.split() if s.isdigit()]
          number_reviews = number_reviews_ratings_list[0]
          number_ratings = number_reviews_ratings_list[1]


          reviews_link = number_reviews_div.css("a.a-text-bold::attr(href)").get() 
          reviews_link = response.urljoin(reviews_link)


          tech_details1_table  = response.css("#productDetails_techSpec_section_1")
          tech_details1_keys   = tech_details1_table.css("th.prodDetSectionEntry")
          tech_details1_values = tech_details1_table.css("td.a-size-base")

          tech_details1 = {}
          for i in range(len(tech_details1_keys)):
               text_keys   = tech_details1_keys[i].css("::text").get()
               text_values = tech_details1_values[i].css("::text").get()

               text_keys   = text_keys.strip()
               text_values = text_values.strip()

               tech_details1[text_keys] = text_values


          tech_details2_table  = response.css("#productDetails_techSpec_section_2")
          tech_details2_keys   = tech_details2_table.css("th.prodDetSectionEntry")
          tech_details2_values = tech_details2_table.css("td.a-size-base")

          tech_details2 = {}
          for i in range(len(tech_details2_keys)):
               text_keys   = tech_details2_keys[i].css("::text").get()
               text_values = tech_details2_values[i].css("::text").get()

               text_keys   = text_keys.strip()
               text_values = text_values.strip()

               tech_details2[text_keys] = text_values

          tech_details = {**tech_details1 , **tech_details2}          


          reviews = []
          yield response.follow(reviews_link,
                                self.parse_reviews,
                                meta={
                                   'url': response.request.url,
                                   'ASIN': ASIN,
                                   'price': price,
                                   'average_customer_reviews': average_customer_reviews,
                                   'number_reviews': number_reviews,
                                   'number_ratings': number_ratings,
                                   'tech_details': tech_details,
                                   'reviews_link': reviews_link,
                                   'reviews': reviews,
                                })


          # next_page = response.css("#pagnNextLink::attr(href)").get()
          # if next_page is not None:
          #      next_page = response.urljoin(next_page)
          #      yield scrapy.Request(next_page, callback=self.parse)


     def parse_reviews(self, response):
          def extract_with_css(query):
               return response.css(query).get(default='').strip()
               
          # reviews = []
          reviews = response.meta['reviews']
          review  = {}
          reviews_list = response.css("div.aok-relative")
          for i in range(len(reviews_list)):
               name = reviews_list[i].css("span.a-profile-name::text").get()
               rating  = reviews_list[i].css("span.a-icon-alt::text").get()
               date  = reviews_list[i].css("span.review-date::text").get()
               title_div = reviews_list[i].css("a.a-text-bold")
               title = title_div.css("span::text").get()
               review_div = reviews_list[i].css("span.review-text-content")
               review_text = review_div.css("span::text").getall()
               review_text = " ".join(review_text)
               review_text = review_text.strip()

               review["name"]   = name
               review["rating"] = rating
               review["date"]   = date
               review["title"]  = title
               review["review_text"] = review_text

               reviews.append(review.copy())


               #yield {
               #     'reviews': review,
               #}


          # follow pagination links
          pagination = response.css("#cm_cr-pagination_bar")
          next_page_div = pagination.css("li.a-last")
          next_page = next_page_div.css("a::attr(href)").get()
          next_page = response.urljoin(next_page)


          if (next_page is not None
              and next_page != response.request.url
              and len(reviews) <= 100):

               yield response.follow(next_page,
                                     self.parse_reviews,
                                     meta={
                                        'reviews': reviews,
                                        'url': response.meta['url'],
                                        'ASIN': response.meta['ASIN'],
                                        'price': response.meta['price'],
                                        'average_customer_reviews': response.meta['average_customer_reviews'],
                                        'number_reviews': response.meta['number_reviews'],
                                        'number_ratings': response.meta['number_ratings'],
                                        'tech_details': response.meta['tech_details'],
                                        'reviews_link': response.meta['reviews_link'], 
                                     })
          else:
               yield {
                    'url': response.meta['url'],
                    'ASIN': response.meta['ASIN'],
                    'price': response.meta['price'],
                    'average_customer_reviews': response.meta['average_customer_reviews'],
                    'number_reviews': response.meta['number_reviews'],
                    'number_ratings': response.meta['number_ratings'],
                    'tech_details': response.meta['tech_details'],
                    'reviews_link': response.meta['reviews_link'], 
                    'reviews': response.meta['reviews'],
               }
               reviews = []



          # for href in response.css('li.next a::attr(href)'):
          #      yield response.follow(next_page, self.parse)     






# Revisar esto:
# https://www.amazon.com/ASUS-Ultra-Thin-Processor-L203MA-DS04-Microsoft/dp/B07N6S4SY1
# List Price        $249.99
# Deal of the Day:  $169.00
     
# Ends in 12h 10m 14s
# You Save: $80.99 (32%) 



