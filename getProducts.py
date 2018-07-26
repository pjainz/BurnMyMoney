from selenium import webdriver
import random
import re
from amazonproduct import API, ResultPaginator, AWSError
from config import AWS_KEY, SECRET_KEY

upperbound = 10
lowerbound = 5

def price_offers(asin):
    api = API(AWS_KEY, SECRET_KEY, 'de')
    str_asin = str(asin)
    node = api.item_lookup(id=str_asin, ResponseGroup='Offers', Condition='All', MerchantId='All')
    for a in node.Items.Item.Offers.Offer:
        print(a.OfferListing.Price.FormattedPrice)

category = ["37e2e580-8091-4621-b9c3-237f6f9f2af4/ref=strm_theme_omg",
			"2ad85be4-a868-4c09-be6f-caa113ce00b3/ref=strm_theme_fun",
			"2a20eb09-13b8-40b9-9e3c-21f550c65b7d/ref=strm_theme_lighting",
			"97e677d7-5f5a-4d2f-956b-76a1aace6291/ref=strm_theme_bigkids",
			"a696266e-739b-47d1-a388-26f2a4c28068/ref=strm_theme_smart-home",
			"80edd9ee-ae64-4dfe-8db8-eb3d745f2094/ref=strm_theme_gadgets",
			"b17742dd-333a-435e-8401-63bc3c8a7e5f/ref=strm_theme_creatures",
			"fefa9ffd-f1da-4bf9-8120-269d6ba2fc68/ref=strm_theme_awww",
			"b2708edf-9836-4f1e-a187-4fe6a4b6c177/ref=strm_theme_skateboards",
			"5e7459f2-00dc-46da-a2a1-6c4babf6870c/ref=strm_theme_mid-century-modern",
			"37b897db-eae1-4e7f-a1f5-01feae5e504a/ref=strm_theme_plush",
			"f9d1f6e7-e775-42ff-9823-d074baa7f2f8/ref=strm_theme_travel",
			"b77c52a5-4e15-4001-a236-88facaff49ff/ref=strm_theme_everyday-carry",
			"37118141-e90a-4939-81ab-6132ab7505f6/ref=strm_theme_sunglasses",
			"88d268c0-858f-4859-9b1a-7ecd8c6f1014/ref=strm_theme_pets",
			"cd7be774-51ef-4dfe-8e97-1fdec7357113/ref=strm_theme_kitchen",
			"cef37a33-8b25-457a-862d-0a626d33cf67/ref=strm_theme_lol",
			"339533ec-598e-4a1a-9cb2-a5215d059323/ref=strm_theme_audio",
			"2d3e5df6-f132-4429-91bb-0d518808eb14/ref=strm_theme_rad",
			"febe881f-18ed-4e7a-bac7-02ed73b9dedc/ref=strm_theme_photo",
			"be4f5c11-9149-4692-a36d-40677358d181/ref=strm_theme_home",
			"e458915a-3a9a-4df8-8d8d-6ef769e58a53/ref=strm_theme_planters",
			"0ee129b6-20d0-4bc1-b100-5fadf9e625b3/ref=strm_theme_workspace",
			"4bdfb0c4-6cb6-4abf-a990-07eb781da676/ref=strm_theme_watches",
			"6facbe3d-85ee-4bde-94af-b487927c7c70/ref=strm_theme_wood"
		   ]

baseurl = "https://www.amazon.com/"
driver = webdriver.PhantomJS(executable_path = '/Users/jainpr/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
asins = []

for c in category:
	driver.get(baseurl + "stream/" + c)
	html = driver.execute_script("return document.documentElement.innerHTML;")
	finder = re.compile('data-fling-asin=&quot;([a-zA-Z0-9]*)&quot;')
	temp = finder.findall(html)
	for t in temp:
		price_offers(t)
	asins.extend(temp)


