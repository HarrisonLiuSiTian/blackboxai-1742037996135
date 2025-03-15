import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict, Optional
from logger import get_logger
from urllib.parse import quote

logger = get_logger()

class ScrapingError(Exception):
    """Custom exception for scraping errors"""
    pass

class BaseScraper:
    def __init__(self, config: dict):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        if config.get('proxy'):
            self.session.proxies.update(config['proxy'])
        self.timeout = config.get('timeout', 30)
        self.retries = config.get('retries', 3)

    def _make_request(self, url: str, method: str = 'GET', **kwargs) -> requests.Response:
        """Make HTTP request with retry logic"""
        for attempt in range(self.retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}/{self.retries}): {str(e)}")
                if attempt == self.retries - 1:
                    raise ScrapingError(f"Failed to fetch {url} after {self.retries} attempts")
                time.sleep(2 ** attempt)  # Exponential backoff

class ToutiaoScraper(BaseScraper):
    def search(self, keyword: str) -> List[Dict]:
        """Search Toutiao for articles matching keyword"""
        encoded_keyword = quote(keyword)
        url = f"{self.config['websites']['toutiao']}/search?keyword={encoded_keyword}"
        
        try:
            response = self._make_request(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Note: This is a basic implementation. The actual scraping logic
            # would need to be adjusted based on Toutiao's actual HTML structure
            for article in soup.find_all('div', class_='article-item'):
                results.append({
                    'title': article.find('a', class_='title').text.strip(),
                    'url': article.find('a', class_='title')['href'],
                    'snippet': article.find('div', class_='abstract').text.strip(),
                    'source': 'toutiao',
                    'timestamp': time.time()
                })
            
            return results
        except Exception as e:
            logger.error(f"Error scraping Toutiao: {str(e)}")
            return []

class BaiduScraper(BaseScraper):
    def search(self, keyword: str) -> List[Dict]:
        """Search Baidu for articles matching keyword"""
        encoded_keyword = quote(keyword)
        url = f"{self.config['websites']['baidu']}/s?wd={encoded_keyword}"
        
        try:
            response = self._make_request(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='result'):
                results.append({
                    'title': result.find('h3').text.strip(),
                    'url': result.find('h3').find('a')['href'],
                    'snippet': result.find('div', class_='c-abstract').text.strip(),
                    'source': 'baidu',
                    'timestamp': time.time()
                })
            
            return results
        except Exception as e:
            logger.error(f"Error scraping Baidu: {str(e)}")
            return []

class GoogleScraper(BaseScraper):
    def search(self, keyword: str) -> List[Dict]:
        """Search Google for articles matching keyword"""
        encoded_keyword = quote(keyword)
        url = f"{self.config['websites']['google']}/search?q={encoded_keyword}"
        
        try:
            response = self._make_request(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='g'):
                results.append({
                    'title': result.find('h3').text.strip(),
                    'url': result.find('a')['href'],
                    'snippet': result.find('div', class_='VwiC3b').text.strip(),
                    'source': 'google',
                    'timestamp': time.time()
                })
            
            return results
        except Exception as e:
            logger.error(f"Error scraping Google: {str(e)}")
            return []

class DouyinScraper(BaseScraper):
    def search(self, keyword: str) -> List[Dict]:
        """Search Douyin for posts matching keyword"""
        encoded_keyword = quote(keyword)
        url = f"{self.config['websites']['douyin']}/search/{encoded_keyword}"
        
        try:
            response = self._make_request(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Note: This is a basic implementation. The actual scraping logic
            # would need to be adjusted based on Douyin's actual structure
            for post in soup.find_all('div', class_='video-card'):
                results.append({
                    'title': post.find('div', class_='title').text.strip(),
                    'url': post.find('a')['href'],
                    'author': post.find('span', class_='author').text.strip(),
                    'source': 'douyin',
                    'timestamp': time.time()
                })
            
            return results
        except Exception as e:
            logger.error(f"Error scraping Douyin: {str(e)}")
            return []

class XiaohongshuScraper(BaseScraper):
    def search(self, keyword: str) -> List[Dict]:
        """Search Xiaohongshu for posts matching keyword"""
        encoded_keyword = quote(keyword)
        url = f"{self.config['websites']['xiaohongshu']}/search?keyword={encoded_keyword}"
        
        try:
            response = self._make_request(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Note: This is a basic implementation. The actual scraping logic
            # would need to be adjusted based on Xiaohongshu's actual structure
            for post in soup.find_all('div', class_='note-item'):
                results.append({
                    'title': post.find('div', class_='title').text.strip(),
                    'url': post.find('a')['href'],
                    'author': post.find('span', class_='author').text.strip(),
                    'source': 'xiaohongshu',
                    'timestamp': time.time()
                })
            
            return results
        except Exception as e:
            logger.error(f"Error scraping Xiaohongshu: {str(e)}")
            return []

def create_scrapers(config: dict) -> Dict:
    """
    Factory function to create instances of all scrapers
    """
    return {
        'toutiao': ToutiaoScraper(config),
        'baidu': BaiduScraper(config),
        'google': GoogleScraper(config),
        'douyin': DouyinScraper(config),
        'xiaohongshu': XiaohongshuScraper(config)
    }
