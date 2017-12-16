import random
import socket
import urllib.request
import urllib.parse
import json
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup

headers = {
    'Referer': 'http://www.xicidaili.com/nn/',
    'User-Agent': '"Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36"'
}

