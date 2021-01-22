import requests
import json

url = 'http://127.0.0.1:8080'

print('GET Requests:')

print('\nTime in server zone -\t' + requests.get(url).text)

print('\nTime in time zone -\t' + requests.get(url+'/America/Toronto').text)

print('\nTime in time zone -\t' + requests.get(url+'/Narnia').text)


print('\nPOST Requests:')

data = {'tz_start': 'America/Toronto', 'type': 'date'}
print('\nDate -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'America/Toronto', 'type': 'time'}
print('\nTime -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'America/Toronto', 'tz_end': 'Europe/Moscow', 'type': 'datediff'}
print('\nDifference -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Indian/Christmas', 'tz_end': 'America/Detroit', 'type': 'datediff'}
print('\nDifference -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Europe/Moscow', 'tz_end': 'America/Detroit'}
print('\nDifference -\t' + requests.post(url=url, data=json.dumps(data)).text)