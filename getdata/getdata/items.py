# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetVOZdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NumberPage = scrapy.Field()
    NameContent = scrapy.Field()
    DataUserId = scrapy.Field()
    DataUserName = scrapy.Field()
    ReplyTime = scrapy.Field()
    ReplyText = scrapy.Field()
    ReplyId = scrapy.Field()
    QuoteFull = scrapy.Field()
    QuoteBlockId = scrapy.Field()
    QuoteBlockText = scrapy.Field()
    QuoteDataSource = scrapy.Field()
    FullText = scrapy.Field()
    pass
