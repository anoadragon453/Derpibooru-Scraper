# Derpibooru parsing bot
# Delivering your pictures on demand!
# Created by Andrew Morgan (2014)

from twill.commands import *
import urllib
import webbrowser
import mechanize
import os

print "Starting Form entering..."

url = "https://derpibooru.org/users/sign_in"
br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots
br.open(url)

print ""
print ""

print "Show forms..."

print ""

for form in br.forms():
    print "Form name:", form.name
    print form

print ""
print ""

print "Selecting second form...\n"

br.form = list(br.forms())[1]

# Grab User credentials
print "\nPlease enter your Derpibooru email:"
user_email = raw_input()
print "\nEnter your password:"
user_password = raw_input()

print "Selecting email and password controls..."

email_control = br.form.find_control("user[email]")
email_control.value = user_email

password_control = br.form.find_control("user[password]")
password_control.value = user_password

remember_me = br.form.controls[5]
remember_me.value = ["1"]

print "\nSubmitting the form... (Please Wait)\n"

response = br.submit()

images_link_list = []

for link in br.links():
	if "Size:" in link.text:
    	 images_link_list.append(link.url)
    	 print link.url

# Remove duplicates from images_link_list
images_link_list = list(set(images_link_list))

print "\n Downloading all images on first page...\n"

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

			current_working_directoy = os.path.dirname(os.path.realpath(__file__))

			# Check if directory for photos exists, if not, create one:
			if not os.path.exists("%s/Derpibooru_Photos" % current_working_directoy):
    			 os.makedirs("%s/Derpibooru_Photos" % current_working_directoy)

    		# Download and place photos inside photos directory in numberical order
			downloaded_image_name = "%s/Derpibooru_Photos/%d.%s" % (current_working_directoy, image_name_count, view_link.url[-3:])
			urllib.urlretrieve(direct_image_link, downloaded_image_name)
			image_name_count += 1

print "Done."
