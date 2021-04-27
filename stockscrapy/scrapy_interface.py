import os
import json
import time
import random
from scrapy.utils.project import get_project_settings
from scrapyscript import Job, Processor

#Only works on linux, for windows use a file, broker, etc, to return data from spider.

class ScrapyInterface:
    
    def __init__(self, spiders: list = []):
        self.spiders = spiders
        self.jobs =[]
        settings_file_path = 'stockscrapy.stockscrapy.settings' 
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = Processor(settings=get_project_settings())

    def create_jobs(self):
        for spider in self.spiders:
            self.jobs.append(Job(spider))

    def run_jobs(self, results):
        results = self.process.run(self.jobs)

    def run_spider(self, results, spider, *args):
        results = self.process.run([Job(spider,args)])

    def run_spider_with_scheduler(self, results, condition_to_stop, spider, url, *args, time_min_between_execs_ms = 10, time_max_between_execs_ms = 100):
        results = {}
        while not condition_to_stop(results):
            time.sleep(random.randint(time_min_between_execs_ms,time_max_between_execs_ms+1)/1000)
            results = self.process.run([Job(spider, args, url=url)])
            if (len(results) > 0):
                results = results[0]
            else:
                results = {}
