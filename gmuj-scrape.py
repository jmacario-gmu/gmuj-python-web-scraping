# Summary: Program to scrape a list of URLs pages and output the main content HTML to an HTML file and as well as saving all linked stylesheets, javascript files, images, documents to local subfolders
# Details: This program requires a text file in the working directory containing a list of URLs to fetch. Each URL should be on its own line.
# Command line options:
# if you do not specify any parameters, the script will ask you what types of resources you want to save (html, css, js, images, documents)
# you can specify what types of output to save by using any of the following command line arguments, in any combination: "html" "css" "js" "img" "doc"
# you can also use the argument "all" to do all, or "none" to do none. in that case it will only scan but not save anything
# if you want to separate saved files by timestamp, use the argument "time"
# Last Modified: 20200302
# Modified by: JM

### import my base library
from functions import *

def main():
	##
	# Summary: 
	# Details: 
	# Last Modified: 20190702
	# Modified by: JM
	##

	# clear screen (cross platform - cls for windows, clear for linux)
	# os.system('cls' if os.name == 'nt' else 'clear')
	os.system('clear')

	# initialize variables
	bolTimestamp = False
	bolSaveHTML = False
	bolSaveCSS = False
	bolSaveJS = False
	bolSaveImages = False
	bolSaveDocs = False

	# if "all" options was specified, set to do all
	if "all" in sys.argv:
		bolSaveHTML = True
		#print("Saving HTML files.")
		bolSaveCSS = True
		#print("Saving CSS files.")
		bolSaveJS = True
		#print("Saving JavaScript files.")
		bolSaveImages = True
		#print("Saving image files.")
		bolSaveDocs = True
		#print("Saving document files.")
		# did we specify to do timestamps?
		if "time" in sys.argv: bolTimestamp = True
	elif "none" in sys.argv:
		pass
	else:
		# see if arguments were specified
		if len(sys.argv)==1:
			# no arguments specified (the first item in sys.argv is the name of the script)
			# ask the user what to do
			print(bcolors.HEADER + 'Select Options:'+ bcolors.ENDC)
			bolTimestamp = fnIsYes(input('Timestamp output? (Y/N): '))
			bolSaveHTML = fnIsYes(input('Save HTML files? (Y/N): '))
			bolSaveCSS = fnIsYes(input('Save CSS files? (Y/N): '))
			bolSaveJS = fnIsYes(input('Save JavaScript files? (Y/N): '))
			bolSaveImages = fnIsYes(input('Save image files? (Y/N): '))
			bolSaveDocs = fnIsYes(input('Save document files? (Y/N): '))
			print()
		else:
			# determine which options were specified via command line parameters
			if "time" in sys.argv:
				bolTimestamp = True
				#print("Saving HTML files.")
			if "html" in sys.argv:
				bolSaveHTML = True
				#print("Saving HTML files.")
			if "css" in sys.argv: 
				bolSaveCSS = True
				#print("Saving CSS files.")
			if "js" in sys.argv: 
				bolSaveJS = True
				#print("Saving JavaScript files.")
			if "img" in sys.argv: 
				bolSaveImages = True
				#print("Saving image files.")
			if "doc" in sys.argv: 
				bolSaveDocs = True
				#print("Saving document files.")

	# output selected options
	print(bcolors.HEADER + 'Selected Options:'+ bcolors.ENDC)
	# do we have something to do?
	if (bolSaveHTML or bolSaveCSS or bolSaveJS or bolSaveImages or bolSaveDocs):
		
		print(fnTrueFalseGreenRed('HTML',bolSaveHTML) + '\t', end='')
		print(fnTrueFalseGreenRed('CSS',bolSaveCSS) + '\t', end='')
		print(fnTrueFalseGreenRed('JS',bolSaveJS) + '\t', end='')
		print(fnTrueFalseGreenRed('IMAGES',bolSaveImages) + '\t', end='')
		print(fnTrueFalseGreenRed('DOCUMENTS',bolSaveDocs) + '\t', end='')
		print()
		print()

		if bolTimestamp: 
			print("Saving output with timestamp.")
		else:
			print(bcolors.WARNING + "Saving output with no timestamp." + bcolors.ENDC)
		if bolSaveHTML: print("Saving HTML files.")
		if bolSaveCSS: print("Saving CSS files.")
		if bolSaveJS: print("Saving JavaScript files.")
		if bolSaveImages: print("Saving image files.")
		if bolSaveDocs: print("Saving document files.")
	else:
		print(bcolors.WARNING + "Nothing to output. Scan only." + bcolors.ENDC)

	print()

	# set environment variables
	print(bcolors.HEADER + 'Environment variables:'+ bcolors.ENDC)

	# set run timestamp
	strTimestamp=fnTimestamp()
	print('Timestamp: ' + strTimestamp) 

	# set current directory
	current_directory=os.path.dirname(os.path.realpath(__file__))
	print("Working directory: "+current_directory)

	# set text file URL list info
	print('URL list file: '+current_directory+"\\"+urlListFile)
	print()

	# shall we continue?
	if not fnIsYes(input('Continue? (Y/N): ')):
		print(bcolors.WARNING + "Quitting Process" + bcolors.ENDC)
		exit()
	print()

	# Prepare to loop through URLs in URL file
	print(bcolors.HEADER + 'Processing URL(s):'+ bcolors.ENDC)
	print()

	# flush output
	sys.stdout.flush()

	# Open URL list text file for reading
	input_file = open(urlListFile, 'r')
	# Set initial value for URLs processed (lines read)
	count_lines = 0
	# Loop through lines in input file
	for line in input_file:
		# check to see if line begins with a number sign (which indicates a comment)
		# TODO: this could be improved to ignore whitespace and comments
		if line[0]!="#":
			# Increment number of lines read
			count_lines += 1
			# Get URL to fetch data from, from current line of text file
			strFetchURL=line.strip()
			
			# Output
			print(bcolors.HEADER + bcolors.UNDERLINE + 'URL: '+strFetchURL + bcolors.ENDC)
			print()

			# get info about URL
			print(bcolors.HEADER + "URL information:" + bcolors.ENDC)
			# get URL protocol
			strFetchURLProtocol=fnGetURLComponent(strFetchURL,"protocol")
			print('Protocol: '+strFetchURLProtocol)
			# get URL domain part
			strFetchURLDomain=fnGetURLComponent(strFetchURL,"domain")
			print('Domain: '+strFetchURLDomain)
			# get URL directory part
			strFetchURLDirectory=fnGetURLComponent(strFetchURL,"directory")
			print('Remote directory: '+strFetchURLDirectory)
			# get URL filename part
			strFetchURLFilename=fnGetURLComponent(strFetchURL,"filename",defaultFilename)
			print("Remote filename: "+strFetchURLFilename)
			# get URL querystring part
			strFetchURLQuerystring=fnGetURLComponent(strFetchURL,"querystring")
			#print("Querystring: "+strFetchURLQuerystring)

			print()

			# figure out where to put it on the local filesystem
			print(bcolors.HEADER + "Local filesystem information:" + bcolors.ENDC)

			#print("Working directory: "+current_directory)

			# set local folder and file info
			
			# set local domain folder
			# start local domain folder string
			strLocalDomainFolder='_scrape-results/'+fnConvertURLToPath(strFetchURLProtocol+"://"+strFetchURLDomain)
			# should we add a timestamp to the folder name?
			if bolTimestamp: strLocalDomainFolder+='-'+strTimestamp
			# finish local domain folder string
			strLocalDomainFolder+='/'
			#print('Local Domain folder: '+strLocalDomainFolder)
			
			# set local path folder
			strLocalFolder=strLocalDomainFolder+strFetchURLDirectory[1:] # clip the directory to remove the leading slash
			#print('Local folder: '+strLocalFolder)
			
			# set local filename
			strLocalFilename=strFetchURLFilename
			# replace first instance of question mark
			strLocalFilename=re.sub(r'\?','-QUERY-',strLocalFilename, 1)
			# clean up the local filename
			strLocalFilename = fnConvertURLToPath(strLocalFilename)
			# append or fix file extension
			# does filename part of URL contain a question mark?
			if "?" in strFetchURLFilename:
				# append html extension
				strLocalFilename+=".html"
			else:
				# rename dynamic files to .html files
				strLocalFilename=re.sub(r'\.(php|cfm)$','.html',strLocalFilename)
			# fix long filenames
			if len(strLocalFilename)>=125:
				#print("I THINK THIS FILENAME IS TOO LONG: " + str(len(strLocalFilename)))
				temp_filename = strLocalFilename[:113] + '-' + fnPadString(str(count_lines),4) + '.html'
				#print("Maybe it should be: " + temp_filename)
				#print("(Which is " + str(len(temp_filename)) + " long)")
				strLocalFilename=temp_filename
			#print('Local filename: '+strLocalFilename)

			# set local path for HTML file
			strLocalPath=strLocalFolder+strLocalFilename
			print('Local file target: '+current_directory+'/'+strLocalPath)
			#print('Local filename: '+strLocalFilename)

			print()

			# Get data from URL
			print(bcolors.HEADER + 'Fetching URL:' + bcolors.ENDC, flush=True)

			# Attempt to get text content response from specified URL
			strResponse=getHTTPResponseContent(strFetchURL)

			# did we get a response?
			if strResponse==False:
				# HTTP request did not respond with with 200 ("OK") response code
				print(bcolors.FAIL + "There was an error accessing this URL. Skipping."+ bcolors.ENDC)
				# set the variable that indicating the save has not been successful
				bolSaveHTMLSuccessful=False
				print()
			else:
				# HTTP request received a 200 ("OK") response code
				print(bcolors.OKGREEN + "200 OK"+ bcolors.ENDC)
				print()
				# output response text
				#print("Response text: " + str(strResponse.encode('utf-8')))

				# Should we save the response text?
				if bolSaveHTML:
					print(bcolors.HEADER + 'Saving URL HTTP response content:' + bcolors.ENDC)

					# reset the variable that indicates whether the save has been successful
					bolSaveHTMLSuccessful=False

					# get directory name(s)
					directory = os.path.dirname(strLocalPath)
					# create directory for this URL, if it doesn't exist
					if not os.path.exists(directory):
						# create directories
						os.makedirs(directory)
						#print("Creating directory: " + directory)
					#else:
					#	#do nothing
					#	#print("Diectory already exists: " + directory)
					# does this file exist?
					#if os.path.exists(strLocalPath):
					#	pass
					#	#print("This path does not exist: " + strLocalPath)
					#else:
					#	pass
					#	#print("This path does exist: " + strLocalPath)
					#print("Current working directory is: " + os.getcwd())

					# save response text
					#print("Attempting to save to: " + strLocalPath)
					try:
						fnOutputStringToFile(strResponse,strLocalPath)
						print(bcolors.OKGREEN + "HTML written to file: "+current_directory+'/'+strLocalPath + bcolors.ENDC)
						bolSaveHTMLSuccessful=True
					except (FileNotFoundError) as e:
						print(bcolors.FAIL + "Unable to write to file: "+current_directory+'/'+strLocalPath + bcolors.ENDC)
						print(e)
						bolSaveHTMLSuccessful=False

					print()


				# Are we doing something that requires parsing the HTML?
				if bolSaveCSS or bolSaveJS or bolSaveImages or bolSaveDocs:

					# parse HTML document to variable using BeautifulSoup
					print(bcolors.HEADER + "Parsing URL HTTP response content:"+ bcolors.ENDC)
					parsedHTMLContent=bs4.BeautifulSoup(strResponse,"html.parser")
					print(bcolors.OKGREEN + "HTML content parsed!" + bcolors.ENDC)
					print()


					# if we are saving stylesheets
					if bolSaveCSS:
						# find stylesheet tags
						print(bcolors.HEADER + 'Finding Stylesheets:' + bcolors.ENDC)

						# initialize image array
						arrSavedStylesheets = []
						# find all stylesheet tags and loop through them
						for stylesheet in parsedHTMLContent.find_all('link', rel='stylesheet'):
							# output current stylesheet source
							print('Stylesheet found: '+stylesheet['href'])

							# get full stylesheet URL
							stylesheetURL = fnGetAbsoluteURL(stylesheet['href'],strFetchURL)
							print('Stylesheet URL: '+stylesheetURL)

							# set the appropriate corresponding local path
							localFilename = fnGetURLLocalPath(stylesheet['href'],strFetchURL,strLocalDomainFolder,strLocalFolder,"CSS")
							print('Local Filename: '+localFilename)

							# do we have this stylesheet URL in the arrSavedStylesheets array already?
							if stylesheetURL in arrSavedStylesheets:
								print(bcolors.WARNING + "This stylesheet has already been saved!" + bcolors.ENDC)
							else:
								# does this file already exist?
								if os.path.exists(localFilename):
									print(bcolors.WARNING + "File already exists. Skipping." + bcolors.ENDC)
								else:
									print("Attempting download...", flush=True)
										
									# get directory name(s)
									directory = os.path.dirname(localFilename)
									#print("Saving to directory: "+directory)
									# if directories don't exist
									if not os.path.exists(directory):
										# make them
										os.makedirs(directory)

									# download and save CSS file
									if fnSaveFileFromURL(stylesheetURL,localFilename,bolShowDetailedHTTPErrors):
										print(bcolors.OKGREEN + "Stylesheet saved!" + bcolors.ENDC)
										# add this URL to the arrSavedStylesheets array
										arrSavedStylesheets.append(stylesheetURL)
									else:
										print(bcolors.FAIL + "Unable to save CSS file." + bcolors.ENDC)
									
							print("", flush=True)

						# output summary information
						print(bcolors.WARNING, end='') if len(arrSavedStylesheets) == 0 else print(bcolors.OKGREEN, end='')
						print("Total stylesheets saved: "+str(len(arrSavedStylesheets)))
						print(bcolors.ENDC, end='')
						print()

					# if we are saving javascripts
					if bolSaveJS:
						# Find javascript file links
						print(bcolors.HEADER + 'Finding Javascript files:' + bcolors.ENDC)
						
						# initialize javascript file array
						arrSavedJavascripts = []
						# find all script tags and loop through them
						for script in parsedHTMLContent.find_all('script', src=True):
							# output current script src
							print("Script found: "+script['src'])
							# does this URL meet the javascript file criteria
							urlMatch = re.search('\.js(\?|$)',script['src'].lower())
							if urlMatch:
								#print("This is a Javascript file. We should download it!")
								
								# get full javascript URL
								javascriptURL = fnGetAbsoluteURL(script['src'],strFetchURL)
								print('Javascript URL: '+javascriptURL)

								# set the appropriate corresponding local path
								localFilename = fnGetURLLocalPath(script['src'],strFetchURL,strLocalDomainFolder,strLocalFolder,"JS")
								print('Local Filename: '+localFilename)

								# do we have this javascript file URL in the arrSavedJavascripts array already?
								if javascriptURL in arrSavedJavascripts:
									print(bcolors.WARNING + "This javascript file has already been saved!" + bcolors.ENDC)
								else:
									# does this file already exist?
									if os.path.exists(localFilename):
										print(bcolors.WARNING + "File already exists. Skipping." + bcolors.ENDC)
									else:
										print("Attempting to download...", flush=True)
										
										# get directory name(s)
										directory = os.path.dirname(localFilename)
										#print("Saving to directory: "+directory)
										# if directories don't exist
										if not os.path.exists(directory):
											# make them
											os.makedirs(directory)

										# download and save javascript file
										if fnSaveFileFromURL(javascriptURL,localFilename,bolShowDetailedHTTPErrors):
											print(bcolors.OKGREEN + "Javascript File saved!" + bcolors.ENDC)
											# add this URL to the arrSavedJavascripts array
											arrSavedJavascripts.append(javascriptURL)
										else:
											print(bcolors.FAIL + "Unable to save Javascript file." + bcolors.ENDC)

							print("", flush=True)

						# output summary information
						print(bcolors.WARNING, end='') if len(arrSavedJavascripts) == 0 else print(bcolors.OKGREEN, end='')
						print("Total Javascript files saved: "+str(len(arrSavedJavascripts)))
						print(bcolors.ENDC, end='')
						print()

					# if we are saving images
					if bolSaveImages:
						# find image links
						print(bcolors.HEADER + 'Finding Images:' + bcolors.ENDC)
						
						# initialize image array
						arrSavedImages = []
						# find all img tags and loop through them
						for img in parsedHTMLContent.find_all('img', src=True):
							# output current image source
							print('Image found: '+img['src'])

							# does this image meet the image file restritction criteria
							urlMatch = re.search(r'^data:',img['src'])
							if not urlMatch:

								# get full image URL
								imageURL = fnGetAbsoluteURL(img['src'],strFetchURL)
								print('Image URL: '+imageURL)

								# set the appropriate corresponding local path
								localFilename = fnGetURLLocalPath(img['src'],strFetchURL,strLocalDomainFolder,strLocalFolder,"images")
								print('Local Filename: '+localFilename)

								# do we have this image URL in the arrSavedImages array already?
								if imageURL in arrSavedImages:
									print(bcolors.WARNING + "This image has already been saved!" + bcolors.ENDC)
								else:
									# does this file already exist?
									if os.path.exists(localFilename):
										print(bcolors.WARNING + "File already exists. Skipping." + bcolors.ENDC)
									else:
										print("Attempting to download...", flush=True)
											
										# get directory name(s)
										directory = os.path.dirname(localFilename)
										#print("Saving to directory: "+directory)
										# if directories don't exist
										if not os.path.exists(directory):
											# make them
											os.makedirs(directory)

										# download and save file
										if fnSaveFileFromURL(imageURL,localFilename,bolShowDetailedHTTPErrors):
											print(bcolors.OKGREEN + "Image saved!" + bcolors.ENDC)
											# add this URL to the arrSavedImages array
											arrSavedImages.append(imageURL)
										else:
											print(bcolors.FAIL + "Unable to save image file." + bcolors.ENDC)
							else:
								print(bcolors.WARNING + "Image doesn't meet criteria. Skipping..." + bcolors.ENDC)

							print("", flush=True)

						# output summary information
						print(bcolors.WARNING, end='') if len(arrSavedImages) == 0 else print(bcolors.OKGREEN, end='')
						print("Total Images saved: "+str(len(arrSavedImages)))
						print(bcolors.ENDC, end='')
						print()

					# if we are saving documents
					if bolSaveDocs:
						# Find document file links
						print(bcolors.HEADER + 'Finding Documents:' + bcolors.ENDC)
						
						# initialize document file array
						arrSavedDocuments = []
						# find all a tags and loop through them
						for a in parsedHTMLContent.find_all('a', href=True):
							# output current a href
							#print("Link found: "+a['href'])
							# does this URL meet the document file criteria
							urlMatch = re.search(fileRegex,a['href'].lower())
							if urlMatch:
								print("Document file found: " + a['href'])

								# get full file URL
								fileURL = fnGetAbsoluteURL(a['href'],strFetchURL)
								print('File URL: '+fileURL)

								# set the appropriate corresponding local path
								localFilename = fnGetURLLocalPath(a['href'],strFetchURL,strLocalDomainFolder,strLocalFolder,"documents")
								print('Local Filename: '+localFilename)

								# do we have this file URL in the arrSavedDocuments array already?
								if fileURL in arrSavedDocuments:
									print(bcolors.WARNING + "This document has already been saved!" + bcolors.ENDC)
								else:
									# does this file already exist?
									if os.path.exists(localFilename):
										print(bcolors.WARNING + "File already exists. Skipping." + bcolors.ENDC)
									else:
										print("Attempting to download...", flush=True)

										# get directory name(s)
										directory = os.path.dirname(localFilename)
										#print("Saving to directory: "+directory)
										# if directories don't exist
										if not os.path.exists(directory):
											# make them
											os.makedirs(directory)

										# download and save file
										if fnSaveFileFromURL(fileURL,localFilename,bolShowDetailedHTTPErrors):
											print(bcolors.OKGREEN + "Document file saved!" + bcolors.ENDC)
											# add this URL to the arrSavedDocuments array
											arrSavedDocuments.append(fileURL)
										else:
											print(bcolors.FAIL + "Unable to save document file." + bcolors.ENDC)

								print("", flush=True)

						# output summary information
						print(bcolors.WARNING, end='') if len(arrSavedDocuments) == 0 else print(bcolors.OKGREEN, end='')
						print("Total document files saved: "+str(len(arrSavedDocuments)))
						print(bcolors.ENDC, end='')
						print()	

			# print completed message
			print(bcolors.HEADER + "URL processing complete!" + bcolors.ENDC)
			print()
			if bolSaveHTML or bolSaveCSS or bolSaveJS or bolSaveImages or bolSaveDocs: 
				print(bcolors.HEADER + "URL Summary:" + bcolors.ENDC)
			if bolSaveHTML: 
				if bolSaveHTMLSuccessful:
					print(bcolors.OKGREEN + "* HTML written to file: "+current_directory+'/'+strLocalPath + bcolors.ENDC)
				else:
					print(bcolors.FAIL + "* Unable to write HTML to file: "+current_directory+'/'+strLocalPath + bcolors.ENDC)
			if bolSaveCSS: print("* Total stylesheets saved: "+str(len(arrSavedStylesheets)))
			if bolSaveJS: print("* Total Javascript files saved: "+str(len(arrSavedJavascripts)))
			if bolSaveImages: print("* Total images saved: "+str(len(arrSavedImages)))
			if bolSaveDocs: print("* Total document files saved: "+str(len(arrSavedDocuments)))

			print()
			print()
			print()


	# print completed message
	print()
	print(bcolors.HEADER + 'Process complete.' + bcolors.ENDC)
	print()
	print('Total number of URLs processed: '+str(count_lines))
	print()
	# make alert sound
	print('\a', end='')

### define global variables

# Set timestamp variable
timestamp = fnTimestamp()
# Text file list of URLs to scrape
urlListFile='input-urls.txt'
# regex to determine which file links to match
fileRegex = "(pdf|docx?|xlsx?|pptx?|zip|msi|dmg|gz)$"
# set default html file name
defaultFilename='index.html'
# show detailed HTTP request errors
bolShowDetailedHTTPErrors=False

### run main function if this file is running as the main program
if __name__ == "__main__":
	main()
