### import libraries

import sys, os, urllib.request, requests, bs4, datetime, re, webbrowser, getpass, time, winsound, argparse
from urllib.error import URLError, HTTPError

### define classes

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

### define functions

## GENERAL

def fnIsYes(inputString):
	##
	# Summary: checks to see if the input is a 'yes' ("y" or "Y" character)
	# Details: 
	# Last Modified: 20170929
	# Modified by: JM
	##

	# check to see if input string represents a yes
	if inputString=='y' or inputString=="Y": 
		varReturn=True
	else: 
		varReturn=False
	# return value
	return varReturn

def fnIfBlankDefaultValue(input_string,default_value):
	##
	# Summary: if the input is blank, use the provided default value
	# Details: 
	# Last Modified: 20190714
	# Modified by: JM
	##

	# is the input string blank?
	if input_string == "":
		return default_value
	else:
		return input_string

## DATE/TIME-RELATED

def fnTimestamp():
	##
	# Summary: returns a timestamp
	# Details: format: YYYYMMDDHHMMSS
	# Last Modified: 20160926
	# Modified by: JM
	##

	# return timestamp
	return '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())

## FILE-RELATED

def fnOutputStringToFile(inputString,outputFileName):
	##
	# Summary: outputs a string to a file
	# Details: string to output and the name of the file to output to are specified as parameters
	# Last Modified: 20161004
	# Modified by: JM
	##

	# this script had been using: open(outputFileName, "w"), but some pages had characters that failed unless in binary mode
	# therefore I am now doing: open(outputFileName, "wb"), 
	# this then requires that the string be encoded as binary, hence the: text_file.write(inputString.encode('utf-8'))
	# prior to switching the file open mode to binary, this encoding was not needed

	# open/create text file for output ("wb" indicates opening file for writing binary data)
	text_file = open(outputFileName, "wb")
	# write output string to file
	text_file.write(inputString.encode('utf-8'))
	# close text file
	text_file.close()

## TEXT-RELATED

def fnPadString(inputString,intLength):
	##
	# Summary: pads a string
	# Details: 
	# Last Modified: 20190720
	# Modified by: JM
	##

	if len(inputString)<intLength:
		# initialize working string
		workingString=inputString
		# while it still needs padding
		while len(workingString)<intLength:
			workingString="0"+workingString
		return workingString
	else:
		return inputString


def fnGetTabs(intNumberOfTabs):
	##
	# Summary: returns a specified number of tab characters
	# Details: 
	# Last Modified: 20190713
	# Modified by: JM
	##	

	# initialize return variable
	return_value=""

	for i in range(intNumberOfTabs):
		return_value+='\t'

	return return_value


def fnTrueFalseGreenRed(inputString,bolValue):
	##
	# Summary: wraps the input string in color codes for green or red, depending on boolean value
	# Details: 
	# Last Modified: 20190713
	# Modified by: JM
	##

	# set color based on boolean status
	if bolValue:
		return_value = bcolors.OKGREEN
	else:
		return_value = bcolors.FAIL
	# append input string
	return_value += inputString
	# reset colors
	return_value += bcolors.ENDC

	return return_value

def fnCheckFirstChar(inputString,specifiedChar):
	##
	# Summary: checks if the last char is a certain specified character
	# Details: 
	# Last Modified: 20190708
	# Modified by: JM
	##

	if inputString[:1]==specifiedChar:
		return True
	else:
		return False

def fnCheckLastChar(inputString,specifiedChar):
	##
	# Summary: checks if the last char is a certain specified character
	# Details: 
	# Last Modified: 20190708
	# Modified by: JM
	##

	if inputString[-1:]==specifiedChar:
		return True
	else:
		return False

## HTTP-RELATED

def good_url_response(strURL):
	##
	# Summary: returns a boolean representing whether this url returned a 200 response or not
	# Details: 
	# Last Modified: 20190731
	# Modified by: JM
	##

	# set user agent string
	strUserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'

	request_headers = {
		'User-Agent': strUserAgent
	}

	# Get HTML document from specified URL
	myResponse=requests.get(strURL, headers=request_headers)
	# check status
	myResponse.raise_for_status
	# print('Status: ' + str(myResponse.status_code))
	# if status is not 200, print message and exit
	if myResponse.status_code!=200:
		# print error
		print (bcolors.FAIL + "Error " + str(myResponse.status_code) + ' ' + myResponse.reason + bcolors.ENDC)
		#print (bcolors.FAIL + myResponse.headers + bcolors.ENDC)
		# return value
		return False
	else:
		return True

def getHTTPResponseContent(strURL):
	##
	# Summary: returns a string representing the HTTP response from a given URL
	# Details: 
	# Last Modified: 20190713
	# Modified by: JM
	##

	# set user agent string
	strUserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'

	request_headers = {
		'User-Agent': strUserAgent
	}

	# Get HTML document from specified URL
	myResponse=requests.get(strURL, headers=request_headers)
	# check status
	myResponse.raise_for_status
	# print('Status: ' + str(myResponse.status_code))
	# if status is not 200, print message and exit
	if myResponse.status_code!=200:
		# print error
		print (bcolors.FAIL + "Error " + str(myResponse.status_code) + ' ' + myResponse.reason + bcolors.ENDC)
		#print (bcolors.FAIL + myResponse.headers + bcolors.ENDC)
		# return value
		return False
	else:
		# output progress message
		#print("URL fetched successfully.")
		# output response text
		#print(myResponse.text)
		# return value
		return myResponse.text

def fnSaveFileFromURL(strURL,strFilename,bolShowDetailedErrors):
	##
	# Summary: given a URL and a local filename, save the file at that URL to the local file
	# Details: 
	# Last Modified: 20190712
	# Modified by: JM
	##

	# set user agent string
	strUserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'

	# replace spaces in URL with %20
	strURL=re.sub(r' ','%20',strURL)

	# set up HTTP request
	myRequest = urllib.request.Request(
	    strURL,
	    data=None, 
	    headers={
	        'User-Agent': strUserAgent
	    }
	)

	# initiate request, checking for errors
	try:
		workingFileURL = urllib.request.urlopen(myRequest)
		workingFile = open(strFilename, 'wb')
		workingFile.write(workingFileURL.read())
		workingFile.close()
		return True
	except HTTPError as e:
		print(bcolors.FAIL + 'HTTP Error: ' + str(e.code) + ' ' + e.reason + bcolors.ENDC)
		if bolShowDetailedErrors: print(bcolors.FAIL + str(e.headers) + bcolors.ENDC, end='')
		return False
	except URLError as e:
	    print(bcolors.FAIL + 'URL Error: ', e.reason , bcolors.ENDC)
	    return False
	except FileNotFoundError as e:
		print(bcolors.FAIL + 'File Not Found Error') 
		print('Errno: ' + str(e.errno) + ' WinError: ' + str(e.winerror) + bcolors.ENDC)
		print(bcolors.FAIL + 'Error String: ' + e.strerror + bcolors.ENDC)
		print(bcolors.FAIL + 'Related file(s): ' + str(e.filename) + ' ' + str(e.filename2) + bcolors.ENDC)

## URL-RELATED

def fnConvertURLToPath(inputString):
	##
	# Summary: cleans-up URLs to remove difficult characters
	# Details: replaces special chars in URLs
	# Last Modified: 20190719
	# Modified by: JM
	##

	# create output string
	outputString=inputString
	# replace the ://
	outputString=outputString.replace("://",".")
	# replace other chars
	outputString=re.sub("[\/\?\=\#\_\>\<\:\{\}\']","-",outputString)
	# replace trailing dash
	outputString=re.sub('-$','',outputString)

	# return value
	return outputString

def fnURLIsAbsolutePath(inputString):
	##
	# Summary: returns whether a given URL string is an absolute or relative path within the site root
	# Details: uses fnCheckFirstChar to check the first character of the URL
	# Last Modified: 20190708
	# Modified by: JM
	##

	if fnCheckFirstChar(inputString,"/"):
		return True
	else:
		return False

def fnURLIsDirectory(inputString):
	##
	# Summary: returns whether a given URL string is a directory or an individual file, by seeing if it ends in a slash
	# Details: uses fnCheckLastChar to check the last character of the URL
	# Last Modified: 20190720
	# Modified by: JM
	##

	# first, strip off any querystring
	workingString=re.sub(r'(\?.*)','',inputString)

	# does it end with a slash?
	if fnCheckLastChar(workingString,"/"):
		return True
	else:
		return False

def fnGetURLComponent(strURL,strComponent,defaultFilename="index.html"):
	##
	# Summary: returns a part of the URL as specified by the strComponent argument
	# Details: 
	# Last Modified: 20190720
	# Modified by: JM
	##

	# process and return value based on strComponent
	if strComponent == "protocol":
		# return just the part of the URL representing the protocol
		return (re.search(r'(https?)',strURL).group(1))
	elif strComponent == "domain":
		# return the domain
		# finds the first slash (beyond the http:// or https:// - character 8 should do) and returns everything up to that point
		workingString = strURL[:strURL.find("/",8)]
		#remove the protocol and return value
		return re.sub(r'^https?://','',workingString)
	elif strComponent == "directory":
		# strip any querystring
		workingString=re.sub(r'(\?.*)','',strURL)
		# return the part of the URL representing the directory but not the actual filename
		workingString=(re.search(r'https?://([^/]*)(/.*)',workingString).group(2))
		# get everything up to the final slash
		return(re.search(r'(.*/)(.*)',workingString).group(1))
	elif strComponent == "filename":
		# return the part of the URL representing the actual filename
		# remove anchor part of URL
		workingString=re.sub(r'#.*','',strURL)
		# if the filename is not provided, but query parameters are used, insert the default filename where it woud go
		# for this we are checking to see if we have a "/?" in the URL. querystring with no filename
		workingString = re.sub(r'\/\?','/' + defaultFilename + '?',workingString)
		# if no filename was specified...
		if fnURLIsDirectory(workingString):
			# use the default filename.
			return defaultFilename
		else:
			# does the URL contain a querystring?
			if re.search(r'\?',strURL):
				# this URL contains a querystring. this means that there could be a slash as a query parameter
				# return URL from last slash PRIOR TO A QUESTION MARK to end
				return re.search(r'(.*)/(.*\?.*)',workingString).group(2)
			else:
				# return URL from last slash to end
				return re.search(r'(.*)/(.*)',workingString).group(2)
	elif strComponent == "querystring":
		# return the querystring
		if re.search(r'\?',strURL):
			return re.search(r'(\?.*)',strURL).group(1)
		else:
			return False
	else:
		print("Specified URL component (" + strComponent + ") not recognized.")
		return False

def fnGetAbsoluteURL(strURL,strStartingURL):
	##
	# Summary: given an starting URL and a second URL that may be relative to it, determines the absolute URL
	# Details: strURL stores the URL in question, which can begin with "http://" "https://" "//" "/" or just the relative path. strStartingURL stores the absolute URL that this URL may be relative to
	# Last Modified: 20190712
	# Modified by: JM
	##

	# get info about URL
	strStartingURLProtocol = fnGetURLComponent(strStartingURL,"protocol")
	strStartingURLDomain = fnGetURLComponent(strStartingURL,"domain")
	strStartingURLDirectory = fnGetURLComponent(strStartingURL,"directory")

	# does this URL start with two slashes?
	if re.search("^//",strURL):
		# add the appropriate protocol
		strURL=re.sub('^//',strStartingURLProtocol+'://',strURL)

	# does this URL start with http:// or https://?
	if re.search("^https?://",strURL.lower()):
		# we already have an absolute URL
		final_url=strURL
	else:
		# is this link an absolute or relative URL?						
		if fnURLIsAbsolutePath(strURL):
			# set the URL using the domain part and the url in question
			final_url=strStartingURLProtocol+'://'+strStartingURLDomain+strURL
		else:
			# set the URL using the domain and directory parts and the url in question
			final_url=strStartingURLProtocol+'://'+strStartingURLDomain+strStartingURLDirectory+strURL

	return final_url

def fnGetURLLocalPath(strURL,strStartingURL,strLocalFolderBase,strLocalFolder,strResourceType):
	##
	# Summary: 
	# Details: 
	# Last Modified: 20190712
	# Modified by: JM
	##

	# get info about starting URL
	strStartingURLProtocol = fnGetURLComponent(strStartingURL,"protocol")
	strStartingURLDomain = fnGetURLComponent(strStartingURL,"domain")

	# does this URL start with two slashes?
	if re.search("^//",strURL):
		# add the appropriate protocol
		strURL=re.sub('^//',strStartingURLProtocol+'://',strURL)

	# is this an absolute URL? (does it start with http:// or https://)?
	if re.search("^https?://",strURL.lower()):
		# If so, then this is already the complete URL
		# get info about this URL
		strURLProtocol=fnGetURLComponent(strURL,"protocol")
		strURLDomain=fnGetURLComponent(strURL,"domain")
		strURLDirectory=fnGetURLComponent(strURL,"directory")
		strURLFilename=fnGetURLComponent(strURL,"filename")

		# remove the querystring from the filename if necessary
		#strURLFilename=re.sub(r"(.*)\?.*$",r"\1",strURLFilename)

		# so this is an absolute URL, but it is the same domain we are starting from?
		if (strURLProtocol==strStartingURLProtocol) and (strURLDomain==strStartingURLDomain):
			# if so, put this in the normal place in the local filesystem (chop the trailing slash from the strLocalFolderBase variable)
			local_filename=strLocalFolderBase[:-1]+strURLDirectory+strURLFilename
		else:
			# if not, put this in the offsite files folder under this domain
			local_filename=strLocalFolderBase+'_offsite-files/'+strResourceType+'/'+fnConvertURLToPath(strURLProtocol+'://'+strURLDomain)+strURLDirectory+strURLFilename
	else:
		# is this link absolute or relative to the domain root?						
		if fnURLIsAbsolutePath(strURL):
			# set local filename by using the domain part and the resource URL
			local_filename=strLocalFolderBase+strURL[1:]
		else:
			# set local filename by using the directory part and the resource URL
			local_filename=strLocalFolder+strURL

	# remove the querystring from the filename if necessary
	local_filename=re.sub(r"(.*)\?.*$",r"\1",local_filename)

	return local_filename

## OTHER

def fnCleanHTMLContent(inputString):
	##
	# Summary: an example function of cleaning-up HTML
	# Details: uses regex to find and replace parts of the content
	# Last Modified: 20171004
	# Modified by: JM
	##

	# create output string
	outputString=inputString
	# replace newline chars after line break tags
	# outputString=re.sub('<br/>\n','<br/>',outputString)
	# replace table class
	# outputString=re.sub('class="tablepress tablepress-id-\d+"','class="datatable"',outputString)
	# add table style
	# outputString=re.sub('<table class="datatable"','<table class="datatable" style="width:98%;"',outputString)
	# remove table id
	# outputString=re.sub(' id="tablepress-\d+"','',outputString)
	# remove tr classes
	# outputString=re.sub(' class="row-\d+ (odd|even)"','',outputString)
	# remove th and td classes
	# outputString=re.sub(' class="column-\d+"','',outputString)
	# add th styles
	#outputString=re.sub('<th>','<th style="width:20%">',outputString)
	# remove tbody class
	# outputString=re.sub(' class="row-hover"','',outputString)
	# return value
	return outputString
