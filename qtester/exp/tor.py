import urllib.request
from urllib.error import HTTPError
from lxml import html, etree
import os
import sys
sys.path.append('qtester')
from libs.TorCrowler import TorCrawler
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

proxies = [
    '162.243.108.129:1080',
    '159.89.49.60:31264',
    '191.96.42.80:1080',
    '96.44.183.149:55225',
    '216.144.230.233:15993',
    '72.11.148.222:56533',
    '188.226.141.61:1080',
    '51.144.228.148:1080',
    '46.4.96.137:1080',
    '88.198.24.108:1080',
    '198.11.179.15:8080',
    '167.86.118.68:8080',
    '191.242.169.127:9999',
    '159.69.114.213:1080',
    '5.133.197.203:49768',
    '5.133.217.88:4249',
    '212.83.151.240:32613',
    '78.47.206.105:1080',
    '176.9.75.42:1080',
    '5.133.207.84:4353',
    '104.248.63.17:30588',
    '149.90.31.59:1080',
    '116.203.254.92:1080',
    '95.179.200.223:32923',
    '88.220.122.198:39880',
    '109.74.144.130:1080',
    '213.136.89.190:13006',
    '154.16.202.22:1080',
    '104.248.63.15:30588',
    '174.70.241.8:24398',
    '184.178.172.18:15280',
    '45.55.230.207:30405',
    '46.243.183.145:1080',
    '81.19.223.180:1080',
    '204.101.61.82:4145'
]
prox_pos = 0


def gg():
    pass


def main():
    # url = 'https://stackoverflow.com/users/10676716'
    url = 'https://ifconfig.me/ip'

    req = urllib.request.Request(url)
    req.set_proxy('socks5://142.93.170.92:1080', 'https')

    resp = urllib.request.urlopen(req)
    all_text = resp.read()
    print(all_text)
    sys.exit()

    tree = html.fromstring(all_text)

    reached = tree.xpath(
        '//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div/div[1]')[0].text
    ans = tree.xpath(
        '//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]')[0].text
    quest = tree.xpath(
        '//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]')[0].text
    print(f"{reached} {ans} {quest}")


if __name__ == '__main__':
    crawler = TorCrawler(ctrl_pass='mypassword')
    response = crawler.get("https://stackoverflow.com/users/10676716/gmb", headers={'User-Agent': UserAgent().chrome})
    print(str(response))
    tree = html.fromstring(str(response))
    reached = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div/div[1]')[0].text
    ans = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]')[0].text
    quest = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]')[0].text
    print(f"{reached} {ans} {quest}")
    print(type(tree))
