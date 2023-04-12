# import pychrome
# from bs4 import BeautifulSoup
# import requests

# def is_shopify_site(shopify_site_url: str):
#     flag = False
#     data = ""
#     url = shopify_site_url
#     try:
#         response = requests.get(url)
#     except ConnectionError:
#         url = url.replace("www.", "")
#         response = requests.get(url)
#     html_content = response.content
#     soup = BeautifulSoup(html_content, 'html.parser')
#     visible_scripts = soup.find_all('link')
#     for i in list(visible_scripts):
#         data = data + str(i)
#     if "shopify" in data or "myshopify" in data:
#         flag = True
#     else:
#         visible_scripts = soup.find_all('meta')
#         for i in list(visible_scripts):
#             data = data + str(i)
#         if "shopify" in data or "myshopify" in data:
#             flag = True
#         else:
#             visible_scripts = soup.find_all('a')
#             for i in list(visible_scripts):
#                 data = data + str(i)
#             if "shopify" in data or "myshopify" in data:
#                 flag = True
#     return flag

# def handle_request(request):
#     if request['method'] == 'Network.requestWillBeSent':
#         url = request['params']['request']['url']
#         is_shopify = is_shopify_site(url)
#         result = "Yes" if is_shopify else "No"
#         tab_id = request['params']['frameId']
#         target = {'tabId': tab_id}
#         chrome.BrowserAction.setBadgeText(target, {'text': result})

# def start_chrome():
#     # chrome = pychrome.Browser(url="http://127.0.0.1:9222")
#     chrome.Network.requestWillBeSent = handle_request
#     chrome.Network.enable()

# if __name__ == '__main__':
#     chrome = pychrome.Browser(url="http://127.0.0.1:9222")
#     start_chrome()

from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.get('/check')
def check_api():
    url = request.args.get('url', '')
    check = is_shopify_site(url)
    if check:
        return "This is a shopify site!", 200
    else:
        return "This is not a shopify site", 200

def is_shopify_site(shopify_site_url: str):
    flag = False
    data = ""
    url = shopify_site_url
    try:
        response = requests.get(url)
    except ConnectionError:
        url = url.replace("www.", "")
        response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    visible_scripts = soup.find_all('link')
    for i in list(visible_scripts):
        data = data + str(i)
    if "shopify" in data or "myshopify" in data:
        flag = True
    else:
        visible_scripts = soup.find_all('meta')
        for i in list(visible_scripts):
            data = data + str(i)
        if "shopify" in data or "myshopify" in data:
            flag = True
        else:
            visible_scripts = soup.find_all('a')
            for i in list(visible_scripts):
                data = data + str(i)
            if "shopify" in data or "myshopify" in data:
                flag = True
    return flag

if __name__ == '__main__':
    app.run()