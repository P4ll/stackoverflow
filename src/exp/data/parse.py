import urllib.request
import requests
from lxml import html, etree

response = urllib.request.urlopen('https://stackoverflow.com/users/43458')
tree = html.fromstring(response.read())
# print(etree.tostring(tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div/div[1]')[0].text))
# print(tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div/div[1]')[0].text)
a = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div/div[1]')[0].text
a = a.strip('~')
n = float(a.strip('km'))
if a[-1] == 'k':
    n *= 1000
elif a[-1] == 'm':
    n *= 1000000
print(n)
b = 1