# smac_keys replace with code
# print replacement
# comments
# new lines
# mpy 
# js and html


import re
import requests
import htmlmin

FILE_NAME = "code_test"
def minify_py(FILE_NAME):
	with open('{}.py'.format(FILE_NAME), 'r') as f:
		op_lines = []
		f1 = f.read()
		print(f1)
		cmpr = re.compile("'''.*'''", re.DOTALL)
		match = cmpr.findall(f1)
		print(match)
		for m in match:
			print("match1 ", m)
			f1 = f1.replace(m, '')
			#line = line.replace(m, '')

		cmpr = re.compile('""".*"""', re.DOTALL)
		match = cmpr.findall(f1)
		print(match)
		for m in match:
			print("match1 ", m)
			f1 = f1.replace(m, '')


		lines = f1.split("\n")
		for line in lines:
			#print('line ', line)

			match = re.findall(r"^#.*", line)
			for m in match:
				print("match ", m)
				line = line.replace(m, '')

			match = re.findall(r" #.*", line)
			for m in match:
				print("match ", m)
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


			

			#if line == "\n":
			#	line = line.replace("\n", '')

			op_lines.append(line)

		print(lines)
		print("\n\n****\n\n")
		print(op_lines)
		for i in ['', ' ', "\n", "\t"]:
			if i in op_lines:
				#op_lines.remove(i)
				op_lines = list(filter((i).__ne__, op_lines))
		#op_lines.remove("\t")
		#op_lines.remove("\n")
		print(op_lines)
		with open('{}_op.py'.format(FILE_NAME), 'w') as f1:
			f1.write("\n".join(op_lines) )
			f1.close()

		f.close()

JS_MINIFY_URL = 'https://www.toptal.com/developers/javascript-minifier/raw'

def minify_js(file):
	file_name, extension = file.split(".", 1)
	data = {'input': open('{}'.format(file), 'rb').read()}
	response = requests.post(JS_MINIFY_URL, data=data)
	#print(response.text)
	if response.status_code == 200:
		with open("{}.min.{}".format(file_name, extension), "wb") as f:
			f.write(bytes(response.text, "utf-8") )

#minify_js("html/index.html")
def minify_html(file):
	minified = htmlmin.minify(open("{}".format(file), "r").read(), remove_empty_space=True)
	print(minified)
	file_name, extension = file.split(".", 1)
	with open("{}.min.{}".format(file_name, extension), "wb") as f:
		f.write(bytes(minified, "utf-8") )

#minify_html("html/index.html")

minify_py(FILE_NAME)