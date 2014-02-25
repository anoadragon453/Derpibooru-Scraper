# Derpibooru parsing bot
# Delivering your pictures on demand!
# Created by Andrew Morgan (2014)

from twill.commands import *
import sys
import urllib
import urllib2
import webbrowser
import mechanize
import os

'''
url = "http://duckduckgo.com/html"
data = urllib.urlencode({'q': 'Python'})
results = urllib2.urlopen(url, data)
with open("results.html", "w") as f:
    f.write(results.read())
 
webbrowser.open("results.html")

'''

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
print email_control.value

password_control = br.form.find_control("user[password]")
password_control.value = user_password
print password_control.value

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

for link_url in images_link_list:
	print "New image with URL:%s" % link_url
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
'''
br.select_form(name="user[email]")
br["q"] = "python"
res = br.submit()
content = res.read()
with open("mechanize_results.html", "w") as f:
    f.write(content)

webbrowser.open("mechanize_results.html")

'''

'''
# Grab User credentials
print "Enter your username:"
username = sys.stdin.readline()
print "Enter your password:"
password = sys.stdin.readline()

# Log into website
print "Logging in..."

browser = get_browser()

browser.go("https://derpibooru.org/users/sign_in")

browser.add_extra_headers('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')

print browser.get_html()

web_page = urllib2.urlopen("https://derpibooru.org/users/sign_in")
print web_page.read()

'''