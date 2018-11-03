# quotes.toscrape.com

import requests
from bs4 import BeautifulSoup
from random import choice

quotes = []
guesses_left = 4

def get_quotes(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	for quote in soup.find_all("div", class_="quote"):
		# Create a new list for every quote
		q = []
		
		# Store the quote and author in variables, then add them to the list
		quote_text = quote.span.text
		quote_author = quote.span.next_sibling.next_sibling.small.text
		q.append(quote_text)
		q.append(quote_author)

		# Get the url for the authors bio, to extract the information
		url = "http://quotes.toscrape.com"
		urlend = quote.span.next_sibling.next_sibling.a.get("href")
		total_url = url + urlend
		r = requests.get(total_url)
		s = BeautifulSoup(r.text, "html.parser")

		# Construct the first hint, (where author was born and when)
		born = "The author was born "
		for a in s.find("span", class_="author-born-date"):
			born += (a + " ")
		for a in s.find("span", class_="author-born-location"):
			born += a
		q.append(born)

		# Constructing the last two hints
		split_author = quote_author.split(" ")

		hint2 = "The authors first name starts with {}".format(split_author[0][0])
		hint3 = "The authors last name starts with {}".format(split_author[1][0])
		q.append(hint2)
		q.append(hint3)

		# Add the final quote list to the list of quotes
		quotes.append(q)

	# If there's a next button on the page, keep going
	if soup.find("li", class_="next"):
		next_page = soup.find("li", class_="next").a.get("href")
	else:
		next_page = None
	if next_page:
		# Recursively call the method as long as there's a next page to be loaded
		url = "http://quotes.toscrape.com" + next_page
		get_quotes(url)

	return quotes

def hint():
	if guesses_left == 3:
		print(quote[2])
	elif guesses_left == 2:
		print(quote[3])
	else:
		print(quote[4])

def prepare_game():
	print("Preparing quotes...")
	q = get_quotes("http://quotes.toscrape.com")
	quote = choice(q)
	print(quote[0])
	return quote

quote = prepare_game()

while True:
	
	print("Guesses left: {}".format(guesses_left))
	guess = input("Guess who said this: ")
	guesses_left -= 1
	if guess != quote[1]:
		if guesses_left == 0:
			print("Game over!")
			print("Correct answer was {}".format(quote[1]))
			print("Would you like to try again (y/n)? ")
			try_again = input()
			if try_again == "y":
				guesses_left = 4
				quote = prepare_game()
			else:
				break
		else:
			hint()
	elif guess == quote[1]:
		print("Congratulations!")
		print("Would you like to try again (y/n)? ")
		try_again = input()
		if try_again == "y":
			guesses_left = 4
			quote = prepare_game()
		else:
			break
	else:
		hint()

# [[Quote, Author, Hint1, Hint2, Hint3], [Quote, Author, Hint1, Hint2, Hint3], [Quote, Author, Hint1, Hint2, Hint3]...]