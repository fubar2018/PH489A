#!/usr/bin/env python  
'''
This script saves each topic in a bagfile as a csv.

Accepts a filename as an optional argument. Operates on all bagfiles in current directory if no argument provided

Written by Nick Speal in May 2013 at McGill University's Aerospace Mechatronics Laboratory
www.speal.ca

Supervised by Professor Inna Sharf, Professor Meyer Nahon 

'''

import rosbag, sys, csv
import time
import string
import os #for file management make directory
import shutil #for file management, copy file

#verify correct input arguments: 1 or 2
'''
print(len(sys.argv))
if (len(sys.argv) > 3):
	print ("invalid number of arguments:   " + str(len(sys.argv)))
	print ("should be 3: 'bag2csv.py' and 'folderName' and 'bagName'")
	print ("or 2: 'bag2csv.py' and 'bagName'")
	print ("or just 1  : 'bag2csv.py'")
	sys.exit(1)
elif (len(sys.argv) == 3):
	folderOfBagFiles = str([sys.argv[1]][0])
	print (folderOfBagFiles)
	fn = ([sys.argv[2]][0])
	listOfBagFiles = [f for f in os.listdir(folderOfBagFiles) if f == fn]
	if len(listOfBagFiles) == 0:
		raise Exception('File Not Found!')
		sys.exit(1)
	numberOfFiles = "1"
	print ("reading only 1 bagfile: " + str(listOfBagFiles[0]))
elif (len(sys.argv) == 2):
	folderOfBagFiles = [sys.argv[1]]
	listOfBagFiles = [f for f in os.listdir("./"+folderOfBagFiles) if f[-4:] == ".bag"]	#get list of only bag files in specified dir.
	numberOfFiles = str(len(listOfBagFiles))
	print ("reading all " + numberOfFiles + " bagfiles in specified directory:"+ folderOfBagFiles +"\n")
	print ("\n press ctrl+c in the next 10 seconds to cancel \n")
	time.sleep(10)
elif (len(sys.argv) == 1):
	listOfBagFiles = [f for f in os.listdir(".") if f[-4:] == ".bag"]	#get list of only bag files in current dir.
	numberOfFiles = str(len(listOfBagFiles))
	print ("reading all " + numberOfFiles + " bagfiles in current directory: \n")
	for f in listOfBagFiles:
		print (f)
	print ("\n press ctrl+c in the next 10 seconds to cancel \n")
	time.sleep(10)
else:
	print ("bad argument(s): " + str(sys.argv))	#shouldnt really come up
	sys.exit(1)
'''


listOfBagFiles=["2017-11-15-13-36-25.bag", "2017-11-15-13-31-32.bag", "2017-11-29-14-40-33.bag", "2017-11-29-15-10-21.bag"]
numberOfFiles=len(listOfBagFiles)
count = 0
for bagFile in listOfBagFiles:
	count += 1
	print ("reading file " + str(count) + " of  " + str(numberOfFiles) + ": " + bagFile)
	#access bag
	if (len(sys.argv) >= 2):
		bag = rosbag.Bag(bagFile)
		#bag = rosbag.Bag(bagFile)
		bagContents = bag.read_messages()
		bagName = bagFile
		print (bagName)
	else:
		bag = rosbag.Bag(bagFile)
		bagContents = bag.read_messages()
		bagName = bag.filename


	#create a new directory
	folder = string.rstrip(bagName, ".bag")
	try:	#else already exists
		os.makedirs("./" + folder)
	except:
		pass
	shutil.copyfile("./" + bagName, "./" + folder + '/' + bagName)


	#get list of topics from the bag
	listOfTopics = []
	for topic, msg, t in bagContents:
		if topic not in listOfTopics:
			listOfTopics.append(topic)


	for topicName in listOfTopics:
		#Create a new CSV file for each topic
		filename = folder + '/' + string.replace(topicName, '/', '_slash_') + '.csv'
		with open(filename, 'w+') as csvfile:
			filewriter = csv.writer(csvfile, delimiter = ',')
			firstIteration = True	#allows header row
			for subtopic, msg, t in bag.read_messages(topicName):	# for each instant in time that has data for topicName
				#parse data from this instant, which is of the form of multiple lines of "Name: value\n"
				#	- put it in the form of a list of 2-element lists
				msgString = str(msg)
				msgList = string.split(msgString, '\n')
				instantaneousListOfData = []
				for nameValuePair in msgList:
					splitPair = string.split(nameValuePair, ':')
					for i in range(len(splitPair)):	#should be 0 to 1
						splitPair[i] = string.strip(splitPair[i])
					instantaneousListOfData.append(splitPair)
				#write the first row from the first element of each pair
				if firstIteration:	# header
					headers = ["rosbagTimestamp"]	#first column header
					for pair in instantaneousListOfData:
						headers.append(pair[0])
					filewriter.writerow(headers)
					firstIteration = False
				# write the value from each pair to the file
				values = [str(t)]	#first column will have rosbag timestamp
				for pair in instantaneousListOfData:
					if len(pair) > 1:
						values.append(pair[1])
				filewriter.writerow(values)
	bag.close()
print ("Done reading all " + str(numberOfFiles) + " bag files.")
