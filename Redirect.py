import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

n = 0
final_response = response.history[n]
while final_response is not None:
    n = n + 1
    final_response = response.history[n]
    break
print(n)
print(final_response.url)

