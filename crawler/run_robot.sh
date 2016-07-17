#!/bin/bash

echo "------------- crawling $1 begins --------------" >> log
date >> log

cd ~/Projects/robot/crawler
echo "--- Changed dir:" >> log
pwd >> log

source ~/Projects/venv/bin/activate 
echo "--- Activated venv" >> log

echo "--- Starting scraping" >> log
scrapy crawl $1 >> log
echo "--- Scraping ended" >> log

date >> log
echo "------------- crawling $1 ends --------------" >> log
