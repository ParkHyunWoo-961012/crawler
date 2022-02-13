# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from sqlalchemy.orm import sessionmaker
from .dbmaker import Content, db_connect, create_tables
import re


class AllnewscrawlerPipeline():
    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        content = str(item['content'])
        content =content.replace("[","")
        content =content.replace("]","")
        content = content.replace(r'\\n',"")
        content = re.sub(" +"," ", content)
        content = content.replace("'","")
        content = content.replace('"',"")#
        content = content.replace(",","") # 쉼표 제거
        content = content.replace("  +"," ") ## 띄어쓰기만 있는 애들 제거

        if content ==" " or content == "":
            pass
        else:
            article = Content()
            article.id = item['id'] if item['id'] else ''
            article.category = item['category'] if item['category'] else ''
            article.title = item['title'].replace("'", "''") if item['title'] else ''
            article.content = content

        if len(item["created_date"]) == 19:
            article.created_dt = item["created_date"][0:4] \
                                 + '-' \
                                 + item["created_date"][6:8] \
                                 + '-' \
                                 + item["created_date"][10:12] \
                                 + ' ' \
                                 + item["created_date"][14:16] \
                                 + ':' \
                                 + item["created_date"][17:19]

        if len(item["updated_date"]) == 19:
            article.updated_dt = item["updated_date"][0:4] \
                                 + '-' \
                                 + item["updated_date"][6:8] \
                                 + '-' \
                                 + item["updated_date"][10:12] \
                                 + ' ' \
                                 + item["updated_date"][14:16] \
                                 + ':' \
                                 + item["updated_date"][17:19]

        try:
            session.merge(article)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

        return item
