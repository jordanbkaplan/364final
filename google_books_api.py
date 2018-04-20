import requests
import json
api_key='AIzaSyCwtkP5Jw8jtoR0CQ2CXBAdPmgw-Su60pI'
client_id='Ub85txPw80cBPmV-cUR_KA'
def returninfo(search_term):
	searched=search_term.replace(" ","+")
	parms = {"q":searched, 'key':api_key}
	r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
	params_dict=json.loads(r.text)
	return (params_dict)

print (returninfo('American Psycho'))
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print (returninfo("Amercan Psycho")['items'][0]['volumeInfo']['title'])
print (returninfo("Amercan Psycho")['items'][0]['volumeInfo']['authors'][0])
print (returninfo("Amercan Psycho")['items'][0]['volumeInfo']['description'])
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print (returninfo('The Deathly Hallows'))
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print (returninfo("The Deathly Hallows")['items'][0]['volumeInfo']['title'])
print (returninfo("The Deathly Hallows")['items'][0]['volumeInfo']['authors'])
print (returninfo("The Deathly Hallows")['items'][0]['volumeInfo']['description'])
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print (returninfo('Twilight'))
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print ("-----------")
print (returninfo("Twilight")['items'][0]['volumeInfo']['title'])
print (returninfo("Twilight")['items'][0]['volumeInfo']['authors'])
print (returninfo("Twilight")['items'][0]['volumeInfo']['description'])



#this function will take the search term of a book so you can create a book instance with the description that is retreived from this api
#and it will give the authors back as well to populate the authors db
#sample inputs can be seen above or any other book really such as Fight Club or Alice in Wonderland
	