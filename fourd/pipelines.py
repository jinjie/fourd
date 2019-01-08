# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy.http import Request

from scrapy.utils.project import get_project_settings

class FourdPipeline(object):
    
    def __init__(self):
        
        settings = get_project_settings();

        self.conn = MySQLdb.connect(
            user=settings.get('FOURD_DB_USER'),
            passwd=settings.get('FOURD_DB_PASSWORD'),
            db=settings.get('FOURD_DB_NAME'),
            host=settings.get('FOURD_DB_HOST'),
            charset="utf8",
            use_unicode=True
        )

        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):
        
        try:
            self.cursor.execute("""INSERT INTO draws(draw_no, draw_date) VALUES(%s, STR_TO_DATE(%s, '%%a, %%e %%b %%Y'))""", 
                           (item['draw_no'].encode('utf-8'), 
                            item['draw_date'].encode('utf-8')))

            self.cursor.execute("""INSERT INTO numbers(number, draw_no, type) VALUES(%s, %s, 'FIRST')""",
                (item['first'].encode('utf-8'),
                 item['draw_no']))

            self.cursor.execute("""INSERT INTO numbers(number, draw_no, type) VALUES(%s, %s, 'SECOND')""",
                (item['second'].encode('utf-8'),
                 item['draw_no']))

            self.cursor.execute("""INSERT INTO numbers(number, draw_no, type) VALUES(%s, %s, 'THIRD')""",
                (item['third'].encode('utf-8'),
                 item['draw_no']))
                 
            for number in item['starters'] :
                self.cursor.execute("""INSERT INTO numbers(number, draw_no, type) VALUES(%s, %s, 'STARTER')""",
                    (number.encode('utf-8'),
                     item['draw_no']))
                            
            for number in item['consolations'] :
                self.cursor.execute("""INSERT INTO numbers(number, draw_no, type) VALUES(%s, %s, 'CONSOLATION')""",
                    (number.encode('utf-8'),
                     item['draw_no']))

            self.conn.commit()


        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])


        return item
