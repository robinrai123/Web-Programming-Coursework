from flask import Flask, render_template
from flask import request
from datetime import datetime
from datetime import date
import csv

app=Flask(__name__)
@app.route('/')
def home():
		reviewsFile='static//reviews.csv'
		reviewsList= readFile(reviewsFile)
		reviewsListLimited = [reviewsList[0],reviewsList[1],reviewsList[2],reviewsList[3],reviewsList[4]]	#only shows the first five reviews

		return render_template('home.html',reviewsListLimited=reviewsListLimited)

@app.route('/reviews')
def reviews():

		reviewsFile='static//reviews.csv'
		reviewsList= readFile(reviewsFile)

		return render_template('review.html',reviewsList=reviewsList)

@app.route('/review', methods=['POST'])
def addreview():
		reviewsFile='static//reviews.csv'
		reviewsList= readFile(reviewsFile)
		name=request.form[('name')]
		comment=request.form[('comment')]
		if (name == '') or (comment == '') or (name == '' and comment ==''):	#if any fields are empty complain
			failMessage = 'Please enter all fields.'

			return render_template('review.html',reviewsList=reviewsList ,failMessage=failMessage)

		now = date.today()
		today=now.strftime('%d-%m-%Y')
		comment='\"'+comment+'\"'
		blank = ''
		newReviewDetails=[name,comment,today,blank,blank,blank]
		reviewsList.append(newReviewDetails)
		writeFile(reviewsList,reviewsFile)
		confirmMessage = 'Your review has been saved.'

		return render_template('review.html',reviewsList=reviewsList, confirmMessage=confirmMessage)

@app.route('/book')
def book():
		bookFile = 'static//book.csv'                   #specifies file to read
		bookList = readFile(bookFile)                   #reads the file, every row is an item in the array
		dateBookList = readFileDate1(bookFile)			#reads the file, every third item is an item in the array
		bothDates = []

		return render_template('book.html', bookList=bookList, dateBookList=dateBookList)

@app.route('/addbook', methods = ['POST'])
def addbook():

		bookFile = 'static//book.csv'                           #specifies the file
		bookList = readFile(bookFile)                           #reads the file, every row is an item in the array
		dateBookList = readFileDate1(bookFile)					#reads the file, every third item is an item in the array

		bookName = request.form[('name')]                       #makes strings from whats been sent from the form
		bookEmail = request.form[('email')]
		bookDate1 = request.form[('book')]
		bookDate2 = request.form[('book2')]

		if (bookDate1 == '') or (bookDate2 == '') or (bookDate1 == '' and bookDate2 =='') or (bookName == '' and bookEmail == ''):	#if any date fields are empty, or both name and email are empty, return a generic field error message
				failMessage = 'Please enter all fields.'

				return render_template('book.html', bookList=bookList, dateBookList=dateBookList, failMessage=failMessage)

		date1 = datetime.strptime(bookDate1, '%Y-%m-%d')            #convert the date strings into date objects
		date2 = datetime.strptime(bookDate2, '%Y-%m-%d')
		date1year = date1.strftime('%Y')
		date1yearint = int(date1year)
		date1Format = date1.strftime('%d-%m-%Y')                    #reformats the date objects
		date2Format = date2.strftime('%d-%m-%Y')
		totalDays = date2 - date1
		daysInt = int(totalDays.days)
		costMultiplier = 30								#cost per day
		winterMultiplier = 0.75							#cost is multiplied by this if winter
		summerMultiplier = 1.25
		winterStart = datetime(date1yearint, 11, 1)
		summerStart = datetime(date1yearint, 5, 1)

		if (date1 <= winterStart) and (date1 >= summerStart):
			totalCost = costMultiplier * summerMultiplier * daysInt

		else:
			totalCost = costMultiplier * winterMultiplier * daysInt

		totalCostStr = str(totalCost)
		costMessage = 'The cost of your stay will be $'+ totalCostStr + '. If you have any inquiries or regrets, contact us.'
		now = str(date.today())                                 #defines todays date
		today = datetime.strptime(now, '%Y-%m-%d')
		pending = 'Pending'
		fieldInputArray = [bookName,bookEmail,date1Format,date2Format,pending]		#makes an array with the strings and dates as items
		bookDatesArray = [date1Format,date2Format,pending]							#makes an array with the date objects as items

		if (bookEmail == ''):																								#if the email field is empty complain
				failMessage = "We'll need your e-mail I'm afraid"

				return render_template('book.html', bookList=bookList, dateBookList=dateBookList, failMessage=failMessage)

		elif (bookName == ''):																								#if the name field is empty complain
				failMessage = "We'll need your name I'm afraid"

				return render_template('book.html', bookList=bookList, dateBookList=dateBookList, failMessage=failMessage)

		elif (date1 < today):
				failMessage = "You can't book the place in the past."

				return render_template('book.html', bookList=bookList, dateBookList=dateBookList, failMessage=failMessage)

		elif (date1 > date2):																								#if you go back in time throw a specific error message
				failMessage = "The check in date should be before the check out date."

				return render_template('book.html', bookList=bookList, dateBookList=dateBookList, failMessage=failMessage)

		else:                                                           #if everything is fine, add the new values to each list, save the file and refresh the page
				bookList.append(fieldInputArray)						#adds the array to the end of the array of arrays
				dateBookList.append(bookDatesArray)						#adds the array to the end of the array of arrays
				writeFile(bookList, bookFile)							#writes the changes to file

				return render_template('book.html', bookList=bookList, dateBookList=dateBookList, costMessage=costMessage)

@app.route('/attractions')
def attractions():

		return render_template('attractions.html')

@app.route('/admin', methods = ['POST'])
def admin():

		bookFile = 'static//book.csv'                           #specifies the file
		bookList = readFile(bookFile)                           #reads the file, every row is an item in the array
		dateBookList = readFileDate1(bookFile)					#reads the file, every third item is an item in the array
		reviewsFile='static//reviews.csv'
		reviewsList= readFile(reviewsFile)
		reviewsListLimited = [reviewsList[0],reviewsList[1],reviewsList[2],reviewsList[3],reviewsList[4]]
		adminName = request.form[('adminLogin')]                #makes strings from whats been sent from the form
		adminPassword = request.form[('adminPass')]

		if (adminName == '') or (adminPassword == '') or (adminName == '' and adminPassword ==''):	#if any date fields are empty, or both name and email are empty, return a generic field error message
			failMessage = 'Please enter all fields.'

			return render_template('home.html', failMessage=failMessage, reviewsListLimited=reviewsListLimited)

		if (adminName == 'Larry') and (adminPassword == '12345'):          #if the email field is empty complain

			return render_template('admin.html', bookList=bookList)

		else:                                                             #if everything is fine, add the new values to each list, save the file and refresh the page
			failMessage = 'Wrong credentials.'

			return render_template('home.html', failMessage=failMessage, reviewsListLimited=reviewsListLimited)

def readFileDate1(aList):

		with open(aList, 'r') as inFile:

				reader = csv.reader(inFile)								#creates reader object on the file
				List = []												#makes an empty array
				for line in reader:                                     #for every line

						Array = [line[2],line[3],line[4]]               #makes an array, where date 1 is the first item and date 2 is the second
						List.append(Array)                              #add array to the list

		print (List)

		return List

def readFile(aList):
		with open(aList, 'r') as inFile:

				reader = csv.reader(inFile)
				List = [row for row in reader]          #every row is an item on an array

		return List

def writeFile(aList, aFile):
		with open(aFile, 'w', newline='') as outFile:

				writer = csv.writer(outFile)
				writer.writerows(aList)					#writes details to a line to file

		return

if __name__=='__main__':
		app.run(debug=True)