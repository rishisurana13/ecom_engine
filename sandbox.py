import requests
from requests.auth import HTTPBasicAuth
import os
import random
import math

prod_img_urls = {
	"bangle": "https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/117167556_376171323351477_8555989556364653469_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=109&_nc_ohc=BvG1SGIlZakAX9KtqP_&oh=582f23ce7ab0ee7b37ace1766e3b264c&oe=5F570296",
	"necklace": "https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/106919189_566573300894419_7336279306070119083_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=3M3_JpkZHEcAX9rQc9w&oh=d0f9782c506128021a2708454c263501&oe=5F37069D",
	"earrings":"https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/105955427_805223816548833_7066712213754810619_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=109&_nc_ohc=1Nu4IM-CxysAX_xUw39&oh=3fb5864fef6bdaf92fc1625bb6cece58&oe=5F36CB38",
	"bracelet":"https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/117167556_376171323351477_8555989556364653469_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=109&_nc_ohc=BvG1SGIlZakAX9KtqP_&oh=582f23ce7ab0ee7b37ace1766e3b264c&oe=5F570296"
}


URL = "http://localhost:8000/sign-in/"
URL1 = "http://localhost:8000/products/"
product = {
    "title": "hihi",
    "discount": 0.0,
    "description": "This some fire jewels bruh.",
    "price": 10000,
    "quantity": 110,
    "product_type": "necklace",
    "gold_wt": 1.3,
    "diamond_wt": 19.2,
    "image_url":"",

}



def get_admin_token(email,pw, url):
	payload = {
	"email" : email,
	"password": pw
	}	
	r = requests.post(url=url, data=payload)
	r_data = r.json()
	token = r_data["token"]
	return token

# token = get_admin_token('r@s.com', 'rishi1301', URL)
# headers = {'Authorization': f"Token {token}"}
    
# r = requests.post(url=URL1,data=product, headers=headers)
# print(r.json())
# exit()





def gen_prod_listing(title, prod_type):
	prod = {}
	prod["title"] = title[:-4]
	prod["discount"] = 0.0
	prod["description"] = prod_type
	prod["product_type"] = prod_type.lower()
	prod["price"] = float(round(random.randint(20000,1000000),-2))
	prod["quantity"] = 110
	prod["gold_wt"] = float(round(random.randint(1,20),2))
	prod["diamond_wt"] = float(round(random.randint(1,60),2))
	prod["image_url"] = prod_img_urls[prod_type.lower()]
	return prod

def post_listing(listing,token,url):
	
	headers = {'Authorization': f"Token {token}"}
    
	upload_prod = requests.post(url=url,data=listing, headers=headers)

	return upload_prod.status_code






path = '/Users/rishisurana/Desktop/RS-Work/Projects/Business/Surana Bespoke/Final Prod Listing'
token = get_admin_token('r@s.com', 'rishi1301', URL)
errors = []

for subdir in os.listdir(path):
	if subdir == '.DS_Store':
		continue

	for folder_item in os.listdir(os.path.join(path,subdir)):
		if folder_item == '.DS_Store':
			continue
		
		listing = gen_prod_listing(folder_item,subdir)
		code = post_listing(listing,token,URL1)
		if int(code) != int(201):
			errors.append(folder_item)
		
		if int(code) == int(201):
			print(f'uploaded {folder_item} successfully.')

print('Errors: ', errors)









