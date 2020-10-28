import requests

base_url = 'http://localhost:8000'

# Test GET /<tz name>
url_1_1 = '/'
url_1_2 = '/Canada/Central'
url_1_3 = '/America/Sitka'

print ('GET /<tz name>')

request_1_1 = requests.get(base_url + url_1_1)
print ('request 1: ' + request_1_1.text)

request_1_2 = requests.get(base_url + url_1_2)
print ('request 2: ' + request_1_2.text)

request_1_3 = requests.get(base_url + url_1_3)
print ('request 3: ' + request_1_3.text)


# Test POST /api/v1/convert
url_2 = '/api/v1/convert'

print ('\nPOST /api/v1/convert')

request_2_1 = requests.post(base_url + url_2, json = {'date': {"date":"12.20.2021 22:21:05", "tz": "EST"}, 'target_tz': 'America/Ensenada'})
print ('request 1: ' + request_2_1.text)

request_2_2 = requests.post(base_url + url_2, json = {'date': {"date":"05.15.2020 12:31:35", "tz": "Asia/Tehran"}, 'target_tz': 'EET'})
print ('request 2: ' + request_2_2.text)

request_2_3 = requests.post(base_url + url_2, json = {'date': {"date":"02.04.2019 21:04:03", "tz": "Egypt"}, 'target_tz': 'Cuba'})
print ('request 3: ' + request_2_3.text)

# Test POST /api/v1/datediff
url_3 = '/api/v1/datediff'

print ('\nPOST /api/v1/datediff')

request_3_1 = requests.post(base_url + url_3, json = {"first_date":"12.20.2021 22:21:05", "first_tz": "EST", "second_date":"12:30pm 2020-12-01", "second_tz": "Europe/Moscow"})
print ('request 1: ' + request_3_1.text)

request_3_2 = requests.post(base_url + url_3, json = {"first_date":"05.03.2021 12:27:35", "first_tz": "EET", "second_date":"06:20pm 2019-11-03", "second_tz": "Cuba"})
print ('request 1: ' + request_3_2.text)

request_3_3 = requests.post(base_url + url_3, json = {"first_date":"07.15.2019 06:33:55", "first_tz": "Eire", "second_date":"07:00pm 2019-10-03", "second_tz": "Australia/Eucla"})
print ('request 1: ' + request_3_3.text)