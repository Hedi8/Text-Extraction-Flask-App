# Important imports
from app import app
from flask import request, render_template, url_for
import os
import cv2
import numpy as np
from PIL import Image
import random
import string
import pytesseract
from datetime import datetime

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

	# Execute if request is get
	global result
	if request.method == "GET":
		full_filename =  'images/white_bg.jpg'
		return render_template("index.html", full_filename = full_filename)

	# Execute if reuqest is post
	if request.method == "POST":
		image_upload = request.files['image_upload']
		imagename = image_upload.filename
		image = Image.open(image_upload)



		# Printing lowercase
		letters = string.ascii_lowercase
		# Generating unique image name for dynamic image display
		name = ''.join(random.choice(letters) for i in range(10)) + '.png'
		full_filename =  'uploads/' + name

		# Extracting text from image
		custom_config = r'-l eng --oem 3 --psm 6'
		text = pytesseract.image_to_string(image,config=custom_config)

		# Remove symbol if any
		characters_to_remove = "!()@—*“>+-,'|£#%$&^_~"
		new_string = text
		for character in characters_to_remove:
			new_string = new_string.replace(character, "")

		# Converting string into list to dislay extracted text in seperate line
		new_string = new_string.split("\n")


		length_str = len(new_string[1])
		sliced_str = new_string[1][length_str::-1]
		print("The sliced string is:", sliced_str)
		date = sliced_str[0]+sliced_str[1]+sliced_str[2]+sliced_str[3]+sliced_str[4]+sliced_str[5]+sliced_str[6]
		length_str = len(date)
		datefab = date[length_str::-1]
		print(datefab)




		length_str2 = len(new_string[2])
		sliced_str2 = new_string[2][length_str2::-1]
		print("The sliced string is:", sliced_str2)
		date2 = sliced_str2[0] + sliced_str2[1] + sliced_str2[2] + sliced_str2[3] + sliced_str2[4] + sliced_str2[5] + sliced_str2[6]
		length_str2 = len(date2)
		dateexp = date2[length_str2::-1]
		print(datetime.strptime(dateexp, '%m/%Y'))
		if(datetime.strptime(dateexp, '%m/%Y') > datetime.now()):
			print('not expired')
			result = 'not expired'
		# Saving image to display in html
		img = Image.fromarray(image_arr, 'RGB')
		img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

		# Returning template, filename, extracted text
		return render_template('index.html', full_filename = full_filename, text = result)

# Main function
if __name__ == '__main__':
    app.run(debug=True)
