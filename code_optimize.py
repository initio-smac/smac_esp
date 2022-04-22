# smac_keys replace with code
# print replacement
# comments
# new lines
# mpy 
# js and html

import time
import os
import re
import requests
import htmlmin
import mpy_cross
import shutil
from debug.DEVICE.smac_keys import smac_keys

HTML_MINIFY_URL = 'https://www.toptal.com/developers/html-minifier/raw'
JS_MINIFY_URL = 'https://www.toptal.com/developers/javascript-minifier/raw'
CSS_MINIFY_URL = 'https://www.toptal.com/developers/cssminifier/raw'


def mpy_bytecode(file):
	mpy_cross.run(file)



def minify_py(FILE_NAME, input_path, output_path):
	with open(input_path +"/"+ FILE_NAME, 'r') as f:
		op_lines = []
		f1 = f.read()
		#print(f1)
		cmpr = re.compile("'''.*'''", re.DOTALL)
		match = cmpr.findall(f1)
		#print(match)
		for m in match:
			#print("match1 ", m)
			f1 = f1.replace(m, '')
			#line = line.replace(m, '')

		cmpr = re.compile('""".*"""', re.DOTALL)
		match = cmpr.findall(f1)
		#print(match)
		for m in match:
			#print("match1 ", m)
			f1 = f1.replace(m, '')


		lines = f1.split("\n")
		for line in lines:
			if line == "from DEVICE.smac_keys import smac_keys":
				line = ""
			#print('line ', line)

			match = re.findall(r"^#.*", line)
			for m in match:
				#print("match ", m)
				line = line.replace(m, '')

			match = re.findall(r" #.*", line)
			for m in match:
				#print("match ", m)
				line = line.replace(m, '')
				#print(l)

			#match = re.findall(r"print.*", line)
			#for m in match:
			#	print("match ", m)
			#	line = line.replace(m, '')

			'''match = re.search(r'\s.*\s', line)
			if match:
				a = match.span()
				b = line[a[0]:a[1]]
				print( b )
				line = line.replace(b, '')'''
			if (line.strip() == ''):
				line = line.strip()

			# \["[A-Z]+"\]
			match = re.findall(r'smac_keys\["[A-Z_]+"\]', line)
			#if match:
			#	print(line)
			for m in match:
				#print("match ", m)
				line = line.replace(m, '"' + eval(m) + '"' )


			

			#if line == "\n":
			#	line = line.replace("\n", '')

			op_lines.append(line)

		#print(lines)
		#print("\n\n****\n\n")
		#print(op_lines)
		for i in ['', ' ', "\n", "\t"]:
			if i in op_lines:
				#op_lines.remove(i)
				op_lines = list(filter((i).__ne__, op_lines))
		#op_lines.remove("\t")
		#op_lines.remove("\n")
		#print(op_lines)
		with open('{}/{}'.format( output_path,FILE_NAME), 'w') as f1:
			f1.write("\n".join(op_lines) )
			f1.close()

		f.close()

def minify_js(file, input_path, output_path):
	file_name, extension = file.split(".", 1)
	data = {'input': open(input_path+ "/" +file, 'rb').read()}
	response = requests.post(JS_MINIFY_URL, data=data)
	#print(response.text)
	if response.status_code == 200:
		with open("{}/{}".format(output_path, file), "wb") as f:
			f.write(bytes(response.text, "utf-8") )

#minify_js("html/index.html")
def minify_html_2(file):
	minified = htmlmin.minify(open("{}".format(file), "r").read(), remove_empty_space=True)
	print(minified)
	file_name, extension = file.split(".", 1)
	with open("{}/{}".format(output_path ,file), "wb") as f:
		f.write(bytes(minified, "utf-8") )



def minify_html(file, input_path, output_path):
	file_name, extension = file.split(".", 1)
	data = {'input': open(input_path+ "/" +file, 'rb').read()}
	response = requests.post(HTML_MINIFY_URL, data=data)
	if response.status_code == 200:
		with open("{}/{}".format(output_path ,file), "wb") as f:
			f.write(bytes(response.text, "utf-8") )

def minify_css(file, input_path, output_path):
	file_name, extension = file.split(".", 1)
	data = {'input': open(input_path+ "/" +file, 'rb').read()}
	response = requests.post(CSS_MINIFY_URL, data=data)
	if response.status_code == 200:
		with open("{}/{}".format(output_path, file), "wb") as f:
			f.write(bytes(response.text, "utf-8") )



#mpy_bytecode("code_test.py", "DEVICE/code_test2.py")
DEBUG_PATH = "debug"
RELEASE_PATH = "release"


dirs = [ "DEVICE", "DEFAULT", "html", "." ]

def minify_all():
	for mod in dirs:
		for di in os.listdir(DEBUG_PATH + "/" + mod):
			#print(di)
			if not os.path.isdir(di):
				print("minifying ", di)
				try:
					file_name, extension = di.split(".", 1)
					
					pat = mod + "/" +di
					if extension == "py":
						minify_py(pat, DEBUG_PATH, RELEASE_PATH)
						time.sleep(.25)
						mpy_bytecode(RELEASE_PATH+"/"+pat)
						time.sleep(.25)
						try:
							os.remove(RELEASE_PATH+"/"+pat)
							pass
						except Exception as e:
							print("cant remove ", RELEASE_PATH+"/"+pat)
						
					elif extension == "html":
						minify_html(pat, DEBUG_PATH, RELEASE_PATH)
					elif extension == "js":
						minify_js(pat, DEBUG_PATH, RELEASE_PATH)
					elif extension == "css":
						minify_css(pat, DEBUG_PATH, RELEASE_PATH)
					else:
						shutil.copyfile(DEBUG_PATH+"/"+pat, RELEASE_PATH+"/"+pat)
				except Exception as e:
					print(e)

#minify_py("DEVICE/start.py", DEBUG_PATH, RELEASE_PATH)
#minify_py("code_test.py", '.', '.')
#minify_py("web_server_async.py", DEBUG_PATH, RELEASE_PATH)
minify_all()