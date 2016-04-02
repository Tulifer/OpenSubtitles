# -*- coding: utf-8 -*- 

import re

fichier1 = "Nashville S01E07 Lovesick Blues.mkv"
fichier2 = "Game.of.Thrones s01e01.HDTV.XviD-FEVER.avi"
fichier3 = "Downton.Abbey.S01E07.FiNAL.FRENCH.DVDRip.XviD-JMT.avi"
fichier4 = "Awkward.S02E02.HDTV.XviD-AFG.avi"
fichier5 = "Even Stevens - 3x03 - My Best Friends Girlfriend.avi"
fichier6 = "HM3x16 - Jake... Another Little Piece of My Heart.avi"
fichier7 = "How.I.Met.Your.Mother.S02E10.720p.HDTV.ReEnc-Max"
fichier8 = "The.Newsroom.2012.S01E02.480p.HDTV.H264"

print(fichier1)
print(fichier2)
print(fichier3)
print(fichier4)
print(fichier5)
print(fichier6)
print(fichier7)
print(fichier8)
print('\n\n\n')

def extractInfo(nomFichier):
	
	# Le numéro de saison ainsi que le numéro d'épisode sont maintenant indiqué par S et E
	# Le numéro de saison à au moins une longueur de 2 caractères et 3 maximum, l'épisode au minimum 3 caractères (sa change ensuite ^^)
	# Avant on trouvait le x le chiffre avant représente la saison et après l'épisode
	# Donc le numéro de saison comporte 1 caractère et 2 pour le numéro de l'épisode
	# Le Tag se trouve TOUJOURS avant l'extension 
	# Donc pour le récupérer c'est assez facile
	# Si le nom du fichier comporte plus d'un point alors on récupère le mot se trouvant juste avant le dernier point et après le tiret du codec
	#
	# REMARQUE: Attention certaines fois je vais compter le S et le E ainsi que le x mais ceux-ci n'ont rien à voir avec le numéro d'épisode
	# ils permettent juste de récupérer ce que l'on veut
	#
	# Nommage Générique
	# Séries : Titre.xxxx.VOSTFR.QUALITE.CODEC-TEAM
	# DVDRIP : Titre.LANGAGE.DVDRip.CODEC-TEAM
	# FilmHD : Titre.LANGAGE.Résolution.QUALITE.CODEC-TEAM

	info = {'saison':'', 'episode':'', 'nomVideo':''}

	''' SAISON '''

	expression = "S[0-9]*"
	result = re.findall(expression,nomFichier)	

	res = False

	for i in result:
		if len(i) == 3:
			info['saison'] = i
			res = True
			break

	if res == False:

		expression = "s[0-9]*"
		result = re.findall(expression,nomFichier)
		
		for i in result:
			if len(i) == 3:
				info['saison'] = i
				res = True
				break


	if res == False:

		expression = "[0-9]x"
		result = re.findall(expression,nomFichier)
		
		for i in result:
			if len(i) == 2:
				info['saison'] = i
				res = True
				break



	''' EPISODE '''

	expression = "E[0-9]*"
	result = re.findall(expression,nomFichier)	

	res = False

	for i in result:
		if len(i) == 3:
			info['episode'] = i
			res = True
			break

	if res == False:

		expression = "e[0-9]*"
		result = re.findall(expression,nomFichier)
		
		for i in result:
			if len(i) == 3:
				info['episode'] = i
				res = True
				break


	if res == False:

		expression = "x[0-9]*"
		result = re.findall(expression,nomFichier)
		
		for i in result:
			if len(i) == 3:
				info['episode'] = i
				res = True
				break
		
	
	'''  NOM DE LA VIDEO '''

	pos = nomFichier.find(info['saison'])
	info['nomVideo'] = nomFichier[0:pos]

	return info



info1 = extractInfo(fichier1)
info2 = extractInfo(fichier2)
info3 = extractInfo(fichier3)
info4 = extractInfo(fichier4)
info5 = extractInfo(fichier5)
info6 = extractInfo(fichier6)
info7 = extractInfo(fichier7)
info8 = extractInfo(fichier8)

def miseEnForme(info):

	final = {'saison':'', 'episode':'', 'name':''}

	final['saison'] = re.findall('\d+', info['saison'])[0]
	final['episode'] = re.findall('\d+', info['episode'])[0]

	tempo = info['nomVideo']

	tempo = tempo.replace("."," ")
	tempo = tempo.replace("-"," ")
	final['name'] = tempo

	return final

print(miseEnForme(info1))
print(miseEnForme(info2))
print(miseEnForme(info3))
print(miseEnForme(info4))
print(miseEnForme(info5))
print(miseEnForme(info6))
print(miseEnForme(info7))
print(miseEnForme(info8))