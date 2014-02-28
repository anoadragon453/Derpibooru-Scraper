# Derpibooru parsing bot
# Delivering your pictures on demand!
# Created by Andrew Morgan (2014)

from getpass import getpass
import urllib
import webbrowser
import mechanize
import os
import time

# Define global variables
br = mechanize.Browser()

def login():
	print "Starting login process..."

	url = "https://derpibooru.org/users/sign_in"
	br.set_handle_robots(False) # ignore robots
	br.open(url)

	br.form = list(br.forms())[1]

	# Grab User credentials
	print "\nPlease enter your Derpibooru email:"
	user_email = raw_input()
	print "\nEnter your password:"
	user_password = getpass()

	email_control = br.form.find_control("user[email]")
	email_control.value = user_email

	password_control = br.form.find_control("user[password]")
	password_control.value = user_password

	remember_me = br.form.controls[5]
	remember_me.value = ["1"]

	print "\nAttempting login..."

	response = br.submit()

	# Check for successful login
	login_check = 0;
	for link in br.links():
		if "Size:" in link.text:
			login_check = 1
	if login_check == 1:
		print "\nSuccessfully logged in!"
		time.sleep(2)
		chooseaction();
	else:
		print "\nLogin Failed. Retrying..."
		time.sleep(2)
		login();

def downloadimagesfromhomepage():
	images_link_list = []

	for link in br.links():
		if "Size:" in link.text:
		 	 images_link_list.append(link.url)

	# Remove duplicates from images_link_list
	images_link_list = list(set(images_link_list))

	current_working_directory = os.path.dirname(os.path.realpath(__file__))

	print "\nDownloading all images on first page to %s/Derpibooru_Photos.\n" % current_working_directory
	time.sleep(1)

	# Iterate through each image on the first page and grab the 'View' link for each

	image_name_count = 0
	images_link_list_length = len(images_link_list)

	for link_url in images_link_list:
		print "New image with URL:%s  (%d/%d)" % (link_url,image_name_count+1,images_link_list_length) 
		url = "https://derpibooru.org%s" % link_url
		br.open(url)
		for view_link in br.links():
			if view_link.text == "View":
				print "Image URL: %s\n" % view_link.url
				direct_image_link = "http:%s" % view_link.url

				# Check if directory for photos exists, if not, create one:
				if not os.path.exists("%s/Derpibooru_Photos" % current_working_directory):
		 			 os.makedirs("%s/Derpibooru_Photos" % current_working_directory)

		 		# Download and place photos inside photos directory in numberical order
		 		downloaded_image_name = ""

		 		if view_link.url[-4:] == "jpeg":
		 			downloaded_image_name = "%s/Derpibooru_Photos/%d.%s" % (current_working_directory, image_name_count, view_link.url[-4:])
		 		else:
					downloaded_image_name = "%s/Derpibooru_Photos/%d.%s" % (current_working_directory, image_name_count, view_link.url[-3:])

				urllib.urlretrieve(direct_image_link, downloaded_image_name)
				image_name_count += 1

	print "\nFinished downloading images.\n"
	time.sleep(2)
	chooseaction();

def downloadimagesfromfeed():
	print "Downloading images from feed...\n"

	# Navigate to Derpibooru settings page
	url = "http://derpibooru.org/settings"
	response = br.open(url)

	# Grab subscribe_url value
	page_source = response.read()
	subscribe_section = page_source.find('name="subscribe_url"');
	print " subscribe_section is %s" % subscribe_section
	subscribe_url_start = page_source.find('value="',subscribe_section);
	print " subscribe_url_start is %s" % subscribe_url_start
	subscribe_url_end = page_source.find('"',subscribe_url_start + 7);
	print " subscribe_url_end is %s" % subscribe_url_end
	subscribe_url = page_source[subscribe_url_start + 7:subscribe_url_end]
	print " subscribe_url is %s" % subscribe_url

	# Navigate to feed url
	response = br.open(subscribe_url)

	# Grab image urls from page
	images_link_list = []
	br._factory.is_html = True

	for link in br.links():
		images_link_list.append(link.url)

	# Remove duplicates from images_link_list
	images_link_list = list(set(images_link_list))

	# State where to store images
	current_working_directory = os.path.dirname(os.path.realpath(__file__))

	print "\nDownloading all images on feed to %s/Derpibooru_Photos.\n" % current_working_directory
	time.sleep(1)

	# Iterate through each image on the first page and grab the 'View' link for each

	image_name_count = 0
	images_link_list_length = len(images_link_list)

	for link_url in images_link_list:
		print "New image with URL:%s  (%d/%d)" % (link_url,image_name_count+1,images_link_list_length) 
		br.open(link_url)
		for view_link in br.links():
			if view_link.text == "View":
				print "Image URL: %s\n" % view_link.url
				direct_image_link = "http:%s" % view_link.url

				# Check if directory for photos exists, if not, create one:
				if not os.path.exists("%s/Derpibooru_Photos" % current_working_directory):
		 			 os.makedirs("%s/Derpibooru_Photos" % current_working_directory)

		 		# Download and place photos inside photos directory in numberical order
		 		downloaded_image_name = ""

		 		if view_link.url[-4:] == "jpeg":
		 			downloaded_image_name = "%s/Derpibooru_Photos/%d.%s" % (current_working_directory, image_name_count, view_link.url[-4:])
		 		else:
					downloaded_image_name = "%s/Derpibooru_Photos/%d.%s" % (current_working_directory, image_name_count, view_link.url[-3:])

				urllib.urlretrieve(direct_image_link, downloaded_image_name)
				image_name_count += 1

	print "\nFinished downloading images.\n"
	time.sleep(2)
	chooseaction();

def chooseaction():
	print "\nWhat would you like to do?"
	print "1. Download images from home page."
	print "2. Download images from your feed."
	print "3. Exit the program."
	user_choice = raw_input("Enter Choice (1,2,3): ");

	if user_choice == "1" or user_choice.upper() == "ONE":
		downloadimagesfromhomepage();
	elif user_choice == "2" or user_choice.upper() == "TWO":
		downloadimagesfromfeed();
	elif user_choice == "3" or user_choice.upper() == "THREE":
		return;
	else:
		print "\nYour response was not understood.\n"
		time.sleep(1)
		chooseaction();

login();
