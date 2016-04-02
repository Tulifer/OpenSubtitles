# -*- coding: utf-8 -*-

import os
import hashVideo
import openSubtitle

#Fichier vidéos
locVideo = "LOCATION OF VIDEO"
nameFichier = "NAME OF VIDEO"
#taille de la vidéo
taille =os.path.getsize(locVideo)


#Récupération du hash de la vidéo
valueOfHash = hashVideo.calc_file_hash(locVideo)

#Création d'un objeet subtitle avec en paramètre les informations de la vidéo
OS = openSubtitle.OpenSubtitle(valueOfHash,taille,nameFichier)

print ("\n  INFO API \n")
print OS.serverInfo()

#Connexion à l'api
print ("\n  LOGIN \n")
print OS.Login()

#Vérification que le hash de la vidéo est bien présent dans la bdd si ce n'est pas le cas on pourrait le rajouter voir plus bas en commentaire
print (" \n CHECH DU HASH MOVIE PAR OpenSubtitle \n")
if OS.CheckMovieHash() != 'Error':

	print (" \n RECHERCHE DES SOUS-TITRES \n")

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(1) != 'Error':
			OS.DownloadSubtitles()

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(2) != 'Error':
			OS.DownloadSubtitles()

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(3) != 'Error':
			OS.DownloadSubtitles()

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(4) != 'Error':
			OS.DownloadSubtitles()

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(5) != 'Error':
			OS.DownloadSubtitles()


if OS.CheckMovieHash2() != 'Error':

	print (" \n RECHERCHE DES SOUS-TITRES \n")

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(1) != 'Error':
			OS.DownloadSubtitles()

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(2) != 'Error':
			OS.DownloadSubtitles()

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(3) != 'Error':
			OS.DownloadSubtitles()

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(4) != 'Error':
			OS.DownloadSubtitles()

	if OS.chechDLSubtitle('',1) == False:
		if OS.SearchSubtitles(5) != 'Error':
			OS.DownloadSubtitles()

if OS.chechDLSubtitle('',1) == False:
	print('Sous-titre introuvable')

#OS.chechDLSubtitle()

'''#Insertion du hash dans la bdd

print ("\n INSERTION DU HASH \n")
print OS.InsertMovieHash()'''


print("--------------------------------------------------------------\n--------------------------------------------------------------")
print(valueOfHash)
print(OS.CheckMovieHash())



#On sé déconnecte
print OS.Logout()