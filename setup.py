# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'voc_crawler',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = voc_crawler.settings']},
)
