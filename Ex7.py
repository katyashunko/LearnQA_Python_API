import requests

all_methods = [{"method":"GET"},{"method":"POST"},{"method":"PUT"},{"method":"DELETE"}]
n = 0
while n<= 3:
    a = all_methods[n]
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type",params=a)
    print(f"GET + {a['method']} in params: " + response.text)
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=a)
    print(f"POST + {a['method']} in data: " + response.text)
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=a)
    print(f"PUT + {a['method']} in data: " + response.text)
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=a)
    print(f"DELETE + {a['method']} in data: " + response.text)
    n += 1


