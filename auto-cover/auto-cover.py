from subprocess import call


with open('latex/main.tex', 'r') as input_file:

	with open('latex_buffer.tex', 'w') as output_file:

		for line in input_file:
			
			output_file.write(line)


with open('latex_buffer.tex', 'r') as input_file:
	filedata = input_file.read()


print 'Welcome to auto-cover!'
name = raw_input('Enter company name: ')
jobtitle = raw_input('Enter job title: ')
field = raw_input('Enter related industry/products: ')

	
filedata = filedata.replace('COMPANY-NAME', name)
filedata = filedata.replace('JOB-TITLE', jobtitle)
filedata = filedata.replace('FIELD', field)


with open('latex_buffer.tex', 'w') as output_file:
	output_file.write(filedata)

call(["vim latex_buffer.tex"])





