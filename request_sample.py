import requests
from requests.auth import HTTPBasicAuth

url = 'http://127.0.0.1:8000/'
targ_url = 'http://127.0.0.1:8000/cart/92/'

def get_token(email,pw, url):
	payload = {
	"email" : email,
	"password": pw
	}	
	r = requests.post(url=url, data=payload)
	r_data = r.json()
	token = r_data["token"]
	return token


def main():
	token = get_token('aa@a.com','rishi', url + 'sign-in/')

	headers = {'Authorization': f"Token {token}"}
	data = { 'product': 274,'quantity':11, 'order':12 }
	res = requests.patch(url=targ_url, data=data, headers=headers)
	# res = requests.get(url=url + 'cart',headers=headers)
   
	print(res.json())
	print('-----')
	print(token)


main()