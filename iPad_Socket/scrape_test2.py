import requests

base_url = 'https://www.barstoolsports.com/'

r = requests.get(base_url, timeout=5)
print(type(r))


