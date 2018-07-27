import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('WindowShopper').sheet1

shopper = sheet.get_all_records()
print(shopper)

def read (user_id):
	index = 2
	while index < sheet.cell(2,5):
		cell = sheet.cell(index, 1)
		if cell == user_id:
			return sheet.row_values(index)
		index += 1

def write (user_id, pos, low, high):
	index = sheet.cell(2,5)
	row = [user_id, pos, low, high]
	sheet.insert_row(row, index)
	sheet.update_cell(2, 5, index+1)

def updatePos (user_id, pos):
	index = 2
	while index < sheet.cell(2,5):
		cell = sheet.cell(index, 1)
		if cell == user_id:
			sheet.update_cell(index, 2, pos)
		index += 1

def delete (user_id):
	index = 2
	while index < sheet.cell(2,5):
		cell = sheet.cell(index, 1)
		if cell == user_id:
			sheet.delete_row(index)
		index += 1