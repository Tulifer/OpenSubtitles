# -*- coding: utf-8 -*-

import zlib
import random
import base64
import xmlrpclib


class OpenSubtitle:


	# Url de l'api
	url = 'http://api.opensubtitles.org/xml-rpc'
	infoVideo = {'hash':'', 'imdbid':'', 'name':'', 'year':'', 'season':'', 'episode':'', 'size':'', 'hashSub':'', 'nameData':''}
	subHash = []
	#Langue des sous-titres souhaité, avec 0 pour non trouvé et 1 pour trouvé
	language = {'English':0, 'French':0}

	def __init__(self,hashVideo,size,name):
		self.infoVideo['hash'] = hashVideo
		self.infoVideo['size'] = size
		self.infoVideo['nameData'] = name

	def serverInfo(self):
		server = xmlrpclib.Server(self.url)
		return server.ServerInfo()

		#Connexion à l'API
	def Login(self):
		server = xmlrpclib.Server(self.url)
		resp = server.LogIn("","","fr","MyAPP V2")
		self.token = str(resp["token"])
		return (resp)


		#Vérification de l'existence du HASHSUB dans la bdd
	def CheckSubHash(self):
		server = xmlrpclib.Server(self.url)
		resp = server.CheckSubHash(self.token,[self.infoVideo['hashSub']])
		return (resp)


		#Récupération d'info à partir du hash
	def CheckMovieHash(self):
		server = xmlrpclib.Server(self.url)
		resp = server.CheckMovieHash(self.token,[self.infoVideo['hash']])

		if len(resp['data'][self.infoVideo['hash']]) != 0:
			self.infoVideo['imdbid'] = str(resp['data'][self.infoVideo['hash']]['MovieImdbID'])
			self.infoVideo['name'] = str(resp['data'][self.infoVideo['hash']]['MovieName'])
			self.infoVideo['year'] = str(resp['data'][self.infoVideo['hash']]['MovieYear'])
			self.infoVideo['season'] = str(resp['data'][self.infoVideo['hash']]['SeriesSeason'])
			self.infoVideo['episode'] = str(resp['data'][self.infoVideo['hash']]['SeriesEpisode'])
		else:
			resp = 'Error'

		return (resp)


		#Récupération d'info à partir du hash v2
	def CheckMovieHash2(self):
		server = xmlrpclib.Server(self.url)
		resp = server.CheckMovieHash2(self.token,[self.infoVideo['hash']])

		if self.infoVideo['hash'] in resp['data']:
			self.infoVideo['imdbid'] = resp['data'][self.infoVideo['hash']][0]['MovieImdbID']
			self.infoVideo['name'] = resp['data'][self.infoVideo['hash']][0]['MovieName']
			self.infoVideo['year'] = resp['data'][self.infoVideo['hash']][0]['MovieYear']
			self.infoVideo['season'] = resp['data'][self.infoVideo['hash']][0]['SeriesSeason']
			self.infoVideo['episode'] = resp['data'][self.infoVideo['hash']][0]['SeriesEpisode']
		else:
			resp = 'Error'

		return (resp)


		#Recherche des sous-titres
	def SearchSubtitles(self,order):
		server = xmlrpclib.Server(self.url)
		content = []
		if(order == 1):
			content.append( { 'moviehash':self.infoVideo['hash'],
								'moviebytesize':self.infoVideo['size']} )
		elif(order ==2):
			content.append( { 'imdbid':self.infoVideo['imdbid']} )

		elif(order == 3):
			content.append( { 'name':self.infoVideo['name']} )
		elif(order==4):
			content.append( { 'query':self.infoVideo['name'],
								'season':self.infoVideo['season'],
									'episode':self.infoVideo['episode']} )
		else:
			content.append( { 'query':self.infoVideo['nameData']})


		resp = server.SearchSubtitles(self.token, content)

		try:
			for i in range(0,len(resp['data'])):
				self.subHash.append({'id':resp['data'][i]['IDSubtitleFile'],'hashSub':resp['data'][i]['SubHash'],'lang':resp['data'][i]['LanguageName']})
		except:
			resp = 'Error'
		return (resp)

		#Vérification si le sous-titres a été téléchargé
	def chechDLSubtitle(self,lang,type):
		if type == 0:
			if self.language[lang] == 0:
				return False
			else:
				return True
		elif type == 1:
			resp = True

			for lang in self.language.values():
				if lang == 0:
					resp = False
					break
			return (resp)
		else:
			return "Error"

		#Téléchargements des sous-titres
	def DownloadSubtitles(self,):
		server = xmlrpclib.Server(self.url)
		resp= ""

		for j in self.language:
			if self.chechDLSubtitle(j,0) == False:

				for i in range(0,len(self.subHash)):
					if self.subHash[i]['lang'] == j:

						self.language[j] = 1 #Sous-titre trouvé on met donc la valeur à 1

						resp = server.DownloadSubtitles(self.token,[self.subHash[i]['id']])
						resp = base64.standard_b64decode(resp['data'][0]['data'])
						resp = zlib.decompress(resp, 47 )
						rnd = random.randrange(1000,999999)

						name = self.infoVideo['name'].replace("'","_")
						name = self.infoVideo['name'].replace('"',"_")
						sub_file = (j[0:2]).upper()  + name + '_' + str(rnd) + '.srt'

						f = open(sub_file,'wb')
						f.write(resp)
						f.close()
						break
		return ()

		#Insertion du hash de la vidéo sur le site
	def InsertMovieHash(self):
		server = xmlrpclib.Server(self.url)
		content = []
		content.append( { 'moviehash':self.infoVideo['hash'],
								'moviebytesize':self.infoVideo['size'],
									'imdbid':self.infoVideo['imdbid']} )

		self.resp = server.InsertMovieHash(self.token,content)
		return (self.resp)


		#Déconnexion
	def Logout(self):
		server = xmlrpclib.Server(self.url)
		server.LogOut(self.token)
		print "\n LOGOUT"