import requests

all_methods = [{"method":"GET"},{"method":"POST"},{"method":"PUT"},{"method":"DELETE"}]

n = 0
while n<= 3:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type",params=all_methods[n])
    print(f"GET + {all_methods[n]['method']} in params: " + response.text)
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=all_methods[n])
    print(f"POST + {all_methods[n]['method']} in data: " + response.text)
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=all_methods[n])
    print(f"PUT + {all_methods[n]['method']} in data: " + response.text)
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=all_methods[n])
    print(f"DELETE + {all_methods[n]['method']} in data: " + response.text)
    n += 1


