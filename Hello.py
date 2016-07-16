#!/usr/bin/python

#~~telepot
import telepot, time, sys#, serial
#~~die
import random
#~~weather
import  pywapi, string
#ser = serial.Serial('/dev/ttyACM0', 9600)

#~~schedule
from datetime import datetime, date
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

#~~database
import shelve
import io

#~~wikipedia
import wikipedia

#~~google search
import json
import urllib.request, urllib.parse

#~~fortune
from subprocess import check_output

#~~Osob eyes
import cv2
from time import localtime, strftime

#~~Logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('events.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
logger.addHandler(fh)

logger.info("Osob initialized!" )


#TODO: implement log file
def futureSchedule(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	f = io.StringIO()
	sched.print_jobs(out=f)
	f.seek(0)
	text = f.read()
	print(text)
	bot.sendMessage(chat_id, text)
	f.close()

	return 0

def readDB():
	#Search for all databases
	BDlist = []
	for document in os.listdir("./"):
		if document.startswith("BD"):
			BDlist.append(document[:-3])

	print("List of BD:")
	print(BDlist)

	for database in BDlist:
		DB = shelve.open(str(database))
		print(DB.values())

	return 0

def updateScheduler():
	#Search for all databases
	BDlist = []
	for document in os.listdir("./"):
		if document.startswith("BD"):
			BDlist.append(document[:-3])

	for database in BDlist:
		DB = shelve.open(str(database))
		for key in list(DB.keys()):

			#TODO: Fix multiple brithdays
			#if ( DB.has_key(key) ):
			#	DB.pop(key)

			month = int(DB[key][2])
			day = int(DB[key][1])

			if str(date.today().month)+str(date.today().day) > str(month)+str(day):
				sched.add_job(happyBirthday, 'date', run_date=datetime(date.today().year+1, month, day, 15,28,55), args=[str(DB[key][0]),str(key)])
			else:
				sched.add_job(happyBirthday, 'date', run_date=datetime(date.today().year, month, day, 15,28,55), args=[str(DB[key][0]),str(key)])
	return 0

def happyBirthday(userName,chat_id):
	bot.sendMessage(chat_id, "Happy birthday "+userName)
	updateScheduler()
	#TODO: Check utility of function above
	return 0

def gSearch(query,chat_id):
	query = urllib.parse.urlencode({'q': query})
	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
	search_response = urllib.request.urlopen(url)
	search_results = search_response.read().decode("utf8")
	results = json.loads(search_results)
	data = results['responseData']
	hits = data['results']
	bot.sendMessage(chat_id, 'Top %d hits:' % len(hits))
	for h in hits: bot.sendMessage(chat_id, str(h['url']))
	bot.sendMessage(chat_id, 'For more results, see %s' % data['cursor']['moreResultsUrl'])
	return 0

def insertBirthday(msg):
	#Parse info from message
	content_type, chat_type, chat_id = telepot.glance2(msg)

	#Open BD of the group
	birthdayBD = shelve.open("BD"+str(chat_id))

	#Stores user name
	userName = msg['from']['first_name']+" "+msg['from']['last_name']

	#Stores original message
	command = msg['text'].split(' ')


	if(len(command)==3):
		try:
			day = int(command[1])
			month = int(command[2])
		except TypeError:
			print ("Can't convert string to int")
			return 0

		if(day>0 and day<=31 and month>0 and month<=12):
			birthdayBD[str(msg['from']['id'])] = [userName,day,month]
			birthdayBD.close()
			bot.sendMessage(chat_id, "Birthday stored.")
			updateScheduler()
	else:
		bot.sendMessage(chat_id, "Bad formating, try again using '/bday dd mm' \ndd = day \nmm = month ")

	return 0

def randomDeath(chat_id):
	items1 = ["n accordian","n acorn","n anvil","n apple"," ball of yarn"," balloon"," banana"," bandana"," bangle bracelet"," bar of soap"," baseball"," basketball"," battery"," beaded bracelet"," beaded necklace"," bell"," book of jokes"," book of matches"," bottle of glue"," bottle of ink"," bottle of lotion"," bottle of soda"," bottle of sunscreen"," bottle of nail polish"," bottle of perfume"," bottle of pills"," bottle of water"," bouquet of flowers"," bow tie"," box of chalk"," box of crayons"," box of markers"," box of tissues"," bunch of grapes"," butter knife"," camera"," candle"," candleholder"," candy bar"," candy cane"," can of beans"," can of chili"," can of peas"," canteen"," catalogue"," celery stick"," cellphone"," chenille stick"," children's book"," Christmas ornament"," class ring"," clock"," clothes pin"," clothing iron"," coffee mug"," coffee pot"," comb"," comic book"," cookie tin"," cork"," craft book"," credit card"," crown"," dictionary"," domino set"," dragon figurine","n egg timer","n electric guitar","n empty bottle","n empty jar","n empty tin can"," fairy statuette"," feather"," flashlight"," flyswatter"," football"," game cartridge"," game CD"," glass jar"," glass vase"," grocery list"," hair brush"," hair clip"," hair pin"," hair ribbon"," hammer"," hair dryer"," hand bag"," handbasket"," hand fan"," handheld game system"," hand mirror"," harmonica","n ice cream scoop","n incense holder"," jar of jam"," jar of peanut butter"," jar of pickles"," jigsaw puzzle"," key"," keyboard"," keychain"," laser pointer"," lemon"," lighter"," lime"," locket"," magazine"," magnifying glass"," map"," marble"," marionette puppet"," martini glass"," measuring tape"," microphone"," multitool"," music CD"," nail"," necktie"," needle"," notebook"," notepad"," novel","n ocarina","n owl figurine"," pack of cards"," pail"," paintbrush"," pair of binoculars"," pair of dice"," pair of earrings"," pair of glasses"," pair of knitting needles"," pair of pliers"," pair of rubber gloves"," pair of safety goggles"," pair of socks"," pair of sunglasses"," pair of underwear"," pair of water goggles"," paperclip"," pearl necklace"," pen"," pencil"," pencil holder"," pepper shaker"," piano"," pickle"," piece of gum"," pinecone"," plush bear"," plush cat"," plush dinosaur"," plush dog"," plush frog"," plush octopus"," plush pony"," plush rabbit"," plush unicorn"," pocketwatch"," postage stamp"," quartz crystal"," quill"," quilt"," rock"," roll of duct tape"," roll of masking tape"," roll of stickers"," roll of toilet paper"," rope"," rubber band"," rubber stamp"," safety pin"," salt shaker"," scallop shell"," scarf"," screwdriver"," screw"," shirt button"," shopping bag"," soccer ball"," snail shell"," snowglobe"," spatula"," spider figurine"," spool of ribbon"," spool of string"," spool of thread"," spoon"," statuette"," sticker book"," stick of incense"," tea cup"," tea pot"," thimble"," toothbrush"," toothpick"," toy boat"," toy car"," toy plane"," toy robot"," toy soldier"," toy top"," tube of lip balm"," tube of lipstick"," ukelele"," unicorn figurine"," unicorn plush"," unicycle"," USB drive"," vacuum cleaner"," Valentine card"," vampire figurine"," veil"," vinyl record"," wallet"," weathervane"," wedding ring"," whistle"," wine glass"," wishbone"," wizard figurine"," wooden spoon"," wristwatch"]
	items2 = ["n axe"," baseball bat"," bow"," broadsword"," cane"," chainsaw"," club"," crowbar"," dagger"," dirk"," flame thrower"," fork"," gatling gun"," hammer"," hatchet"," hypodermic needle"," katana"," lance"," machete"," pair of nunchaku"," pair of scissors"," pistol"," pocket knife"," rifle"," sickle"," spear"," staff"," steak knife"," stick"," trident"," walking stick"," wand"," whip"," wrench"]
	feel = ["blunt","sharp","sharp and blunt"]
	trauma = ["chest","skull","spinal column"]
	limb = ["arm","hand","leg","foot","carotid artery","radial artery","ulnar artery","brachial artery","femoral artery","anterior tibial artery","posterior tibial artery"]
	blood = ["a broken spinal column","accidental strangulation","an acute allergic reaction","acute appendicitis","an acute bacterial infection","acute food poisoning","acute fungal infection","acute poisoning","an acute viral infection","an aneurysm","asphyxiation","being eaten by a large predator","chronic poisoning","cirrhosis of the liver","complete and instant vaporization","complications caused by an influenza infection","a deadly spiderbite","a deadly sting","dehydration","deliberate exsanguination","deliberate strangulation","deliberate suffocation","drowning","edema in the skull","edema in the lungs","electrocution","a heart attack","Hepatitis C","hyperthermia","hypothermia","injuries sustained from a high fall","internal haemorrhaging","leukemia","long-term exposure to environmental toxins","meningitis","malaria","multiple blunt force injuries","multiple stab wounds","mutilation by a large animal","a parasitic infection","a pulmonary embolism","radiation poisoning","rapid depressurization","a respiratory infection","severe acid burns","severe blood loss resulting from multiple injuries","a severe necrotic infection","smoke inhalation","standing in close proximity to a high-powered explosive detonating","a stroke","syphillis","trauma sustained due to being crushed under an enormous weight","a venomous snakebite","violence-induced pulmonary arrythmia"]

	cause = random.randrange(4)
	if  cause == 1:
		bot.sendMessage(chat_id, "Cause of death was a peculiar incident involving a"+random.choice(items1)+" and a"+random.choice(items2))
	elif cause == 2:
		bot.sendMessage(chat_id, "Death was caused by "+random.choice(feel)+" force trauma to the "+random.choice(trauma))
	elif cause == 3:
		bot.sendMessage(chat_id, "Cause of death was blood loss resulting from a severed "+random.choice(limb))
	elif cause == 4:
		bot.sendMessage(chat_id, "Death was caused by "+random.choice(blood))

def osobEyes(chat_id):
	##VideoCapture object
	cap = cv2.VideoCapture(0)

	_,frame = cap.read()

	font = cv2.FONT_HERSHEY_PLAIN
	cv2.putText(frame, strftime("%Y-%m-%d %H:%M:%S", localtime()), (10,20), font, 1.4, (0,0,0), 1, cv2.LINE_AA)
	cv2.imwrite("test.jpg", frame)

	del(cap)

	# Uploading a file may take a while. Let user know you are doing something.
	bot.sendChatAction(chat_id, 'upload_photo')

	# Use `file_id` to resend the same photo, with a caption this time.
	bot.sendPhoto(chat_id, open('test.jpg', 'rb'), caption='Room')

	return(0)

def handle(msg):

	#print(msg)
	try:
		userName = msg['from']['first_name']+" "+msg['from']['last_name']
	except:
		try:
			userName = msg['from']['first_name']+" LastNameUnkown"
		except:
			userName = "FirstNameUnknown LastNameUnkown"

	content_type, chat_type, chat_id = telepot.glance(msg)

	#print (content_type)
	#print ("---")
	#print (chat_type)
	#print ("---")
	#print (chat_id)
	#print ("---")
	#print(msg)
	#print("----")

	thanksText = ["Think nothing of it.", "You are very welcome", "At your command", "No worries", "That's my job", ":)"]
	helloText = [", any commands for today?", "I'm waiting for instructions", "I hope you're doing well today", ", do you want some more info? use /help"]

	if (content_type == 'text'):
		command = msg['text']
		print ('Got command from '+userName+': %s' % command)

		if  '/hello' in command:
			logger.info(userName+" used "+command )
			#bot.sendMessage(chat_id, "Hello , how are you?")
			bot.sendMessage(chat_id, "Hello "+userName+" "+random.choice(helloText))

		elif "/help" in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, "The available commands are: \n/hello \n/roll <'#dice'd'#faces'>\n/weather <city state>\n/dragao \n/thanks \n/g <query>\n/wikipedia <query> \n/bday <dd> <mm> \n/fortune \n/telephone\n/rpg")

		elif "/wikipedia" in command:
			logger.info(userName+" used "+command )
			if (len(command) > 10):
				query = command[10:]
				summary = wikipedia.summary(query, sentences=3)
				url = wikipedia.page(query).url
				bot.sendMessage(chat_id, summary)
				bot.sendMessage(chat_id, url)
			else:
				bot.sendMessage(chat_id, "To search on wikipedia send \n/wikipedia <querry>")

		elif '/roll' in command:
			logger.info(userName+" used "+command )
			roll = command.split(" ")
			for dies in roll[1:]: #TODO:try catch for more than one command in one line or bad format
				nDies = dies.split("d")[0]
				for rollCounter in range(0,int(nDies)):
					bot.sendMessage(chat_id,"Dice #"+str(rollCounter+1)+": "+str(random.randint(1,int(dies.split("d")[1]))))

		elif '/weather' in command: #TODO: Implement search! Command to search for code: pywapi.get_location_ids("string")
			logger.info(userName+" used "+command )
			searchCity = command.split(" ")

			try:
				searchCity[1] #Checks if there is another argument in the command
				cityInfo = pywapi.get_loc_id_from_weather_com(command[9:])
				weatherResult = pywapi.get_weather_from_yahoo(cityInfo[0][0])
				bot.sendMessage(chat_id, "Está fazendo " + weatherResult['condition']['temp'] + "°C agora em "+cityInfo[0][1]+".\n\n")
			except IndexError:
				print('Default Weather search')
				weatherResult = pywapi.get_weather_from_yahoo('BRXX0312')
				bot.sendMessage(chat_id, "It is " + str(weatherResult['condition']['text']) + " e " + weatherResult['condition']['temp'] + "C now in Tiangua.\n\n")

				weatherResult = pywapi.get_weather_from_yahoo('BRXX3696')
				bot.sendMessage(chat_id, "It is " + str(weatherResult['condition']['text']) + " and " + weatherResult['condition']['temp'] + "C now in Sobral.\n\n")

				weatherResult = pywapi.get_weather_from_yahoo('EIXX0014')
				bot.sendMessage(chat_id, "It is " + str(weatherResult['condition']['text']) + " e " + weatherResult['condition']['temp'] + "C now in Dublin.\n\n")

				weatherResult = pywapi.get_weather_from_yahoo('CAXX0518')
				bot.sendMessage(chat_id, "It is " + str(weatherResult['condition']['text']) + " e " + weatherResult['condition']['temp'] + "C now in Vancouver.\n\n")

		elif '/lamp_on' in command:
			logger.info(userName+" used "+command )
			#ser.write(b'Y')
			bot.sendMessage(chat_id, "The lamp is ON")

		elif '/lamp_off' in command:
			logger.info(userName+" used "+command )
			#ser.write(b'N')
			bot.sendMessage(chat_id, "The lamp is OFF")

		elif '/dragao' in  command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, "dragaosemchama.com.br conhecimento vale ouro!")

		elif '/thanks' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, random.choice(thanksText))

		elif 'biscoito' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, "É bolacha!")

		elif 'bolacha' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, "É biscoito!")

		elif '/bday' in command:
			logger.info(userName+" used "+command )
			insertBirthday(msg)

		elif '/eyes' in command:
		#elif '/4791949435' in command:
			logger.info(userName+" used "+command )
			osobEyes(chat_id)

		elif '/fday' in command:
			logger.info(userName+" used "+command )
			futureSchedule(msg)

		elif '/g' in command:
			logger.info(userName+" used "+command )
			gSearch(command[3:],chat_id)

		elif '/reactions' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, "/shots: SHOTS FIRED\n/flip: (╯°□°）╯︵ ┻━┻\n/shrug: ¯\_(ツ)_/¯\n/lenny: ( ͡° ͜ʖ ͡°)")

		elif '/shots' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, "SHOTS FIRED)")

		elif '/flip' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, " (╯°□°）╯︵ ┻━┻")

		elif '/shrug' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, "¯\_(ツ)_/¯")

		elif '/lenny' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, " ( ͡° ͜ʖ ͡°)")

		elif '/fortune' in command:
			logger.info(userName+" used "+command )
			with open("fortuneDB.txt") as f:
				fortunes = f.read().split("%")

			bot.sendMessage(chat_id, random.choice(fortunes))

		elif '/rpg' in command:
			logger.info(userName+" used "+command )
			randomDeath(chat_id)


		elif '/telephone' in command:
			logger.info(userName+" used "+command )
			with open("answeringMachine.txt") as f:
				hear = f.read().split("%")

			bot.sendMessage(chat_id, random.choice(hear))

		elif '/readDB' in command:
			logger.info(userName+" used "+command )
			readDB()

		elif '/id' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, 				\
				"From: "+userName+				\
				"\nUsername: @"+msg['from']['username']+	\
				"\nChat ID: "+str(msg['chat']['id'])+		\
				"\nChat status: "+chat_type)

		elif '/secret' in command:
			logger.info(userName+" used "+command )
			bot.sendMessage(chat_id, "secret commands: \n open the pod bay doors \n biscoito \n bolacha")


		elif 'open the pod bay doors' in command:
			logger.info(userName+" used "+command )
			# Uploading a file may take a while. Let user know you are doing something.
			bot.sendChatAction(chat_id, 'upload_photo')

			# Use `file_id` to resend the same photo, with a caption this time.
			bot.sendPhoto(chat_id, open('pod_bay_doors.png', 'rb'), caption='Glados')

	else:
		bot.sendMessage(chat_id, "Sorry I don't know how to handle "+content_type+" yet.")

	return 0

if __name__ == '__main__':

	TOKEN = sys.argv[1]  # get token from command-line

	# Create a bot object with API key
	bot = telepot.Bot(TOKEN)

	# Attach a function to notifyOnMessage call back
	bot.message_loop(handle)

	sched = BackgroundScheduler()

	sched.start()

	updateScheduler()

	try:
		# This is here to simulate application activity (which keeps the main thread alive).
		while True:
			time.sleep(2)
	except (KeyboardInterrupt, SystemExit):
		# Not strictly necessary if daemonic mode is enabled but should be done if possible
		sched.shutdown()


