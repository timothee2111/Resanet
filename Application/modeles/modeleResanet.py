#!/usr/bin/python3
# -*- coding: utf-8 -*-


import mysql.connector



connexionBD = None

def getConnexionBD() :
	global connexionBD
	try :
		if connexionBD == None :
			connexionBD = mysql.connector.connect(
					host = 'localhost' ,
					user = 'rsnt' ,
					password = 'azerty' ,
					database = 'resanet'
				)
		return connexionBD
	except :
		return None


def seConnecterGestionnaire(login, mdp):
    try:
        curseur = getConnexionBD().cursor()
        requete = '''
                    select nom,prenom 
                    from Gestionnaire
                    inner join Personnel 
                    on Gestionnaire.matricule = Personnel.matricule
                    where login = %s
                    and mdp = %s
                '''

        curseur.execute(requete, (login, mdp))

        enregistrement = curseur.fetchone()

        if enregistrement is not None:  
            gestionnaire = {
                'login': login,
                'nom': enregistrement[0],
                'prenom': enregistrement[1]
            }
        else:
            gestionnaire = None

        curseur.close()
        return gestionnaire

    except Exception as e:
        print("Une erreur s'est produite :", str(e))
        return None

		
def seConnecterUsager( numeroCarte , mdpCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select solde,activee,nom,prenom 
					from Carte
					inner join Personnel 
					on Carte.matricule = Personnel.matricule
					where numeroCarte = %s
					and mdpCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , mdpCarte ) )
		
		enregistrement = curseur.fetchone()
		
		usager = {}
		if enregistrement != None :
			usager[ 'numeroCarte' ] = numeroCarte
			usager[ 'solde' ] = enregistrement[ 0 ]
			usager[ 'activee' ] = enregistrement[ 1 ]
			# print type( usager[ 'activee' ] )
			usager[ 'nom' ] = enregistrement[ 2 ]
			usager[ 'prenom' ] = enregistrement[ 3 ]
			
		curseur.close()
		return usager
		
	except :
		return None


def getSolde( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select solde
					from Carte
					where numeroCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , ) )
		
		enregistrement = curseur.fetchone()
		
		solde = 'inconnu'
		if enregistrement != None :
			solde = enregistrement[ 0 ]
			#print type(solde)
			
		curseur.close()
		return solde
		
	except :
		return None
		
		
def getTarifRepas( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select tarifRepas
					from Fonction
					inner join Personnel
					on Fonction.idFonction = Personnel.idFonction
					inner join Carte
					on Personnel.matricule = Carte.matricule
					where numeroCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , ) )
		
		enregistrement = curseur.fetchone()
		
		tarif = 'inconnu'
		if enregistrement != None :
			tarif = enregistrement[ 0 ]
			#print type(tarif)
			
		curseur.close()
		return tarif
		
	except :
		return None

def getPersonnelsSansCarte() :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select matricule, nom , prenom , nomService
					from Service
					inner join Personnel
					on Service.idService = Personnel.idService
					where matricule not in ( 
												select matricule
												from Carte
											)
				'''

		curseur.execute( requete , () )
		
		enregistrements = curseur.fetchall()
		
		personnels = []
		for unEnregistrement in enregistrements :
			unPersonnel = {}
			unPersonnel[ 'matricule' ] = unEnregistrement[ 0 ]
			unPersonnel[ 'nom' ] = unEnregistrement[ 1 ]
			unPersonnel[ 'prenom' ] = unEnregistrement[ 2 ]
			unPersonnel[ 'nomService' ] = unEnregistrement[ 3 ]
			personnels.append( unPersonnel )
			
		curseur.close()
		return personnels
		
	except :
		return None
		
def getPersonnelsAvecCarte() :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select Personnel.matricule, solde, activee, nom , prenom , nomService
					from Service
					inner join Personnel
					on Service.idService = Personnel.idService
					inner join Carte
					on Carte.matricule = Personnel.matricule
				'''

		curseur.execute( requete , () )
		
		enregistrements = curseur.fetchall()
		
		personnels = []
		for unEnregistrement in enregistrements :
			unPersonnel = {}
			unPersonnel[ 'matricule' ] = unEnregistrement[ 0 ]
			unPersonnel[ 'solde' ] = unEnregistrement[ 1 ]
			unPersonnel[ 'activee' ] = unEnregistrement[ 2 ]
			unPersonnel[ 'nom' ] = unEnregistrement[ 3 ]
			unPersonnel[ 'prenom' ] = unEnregistrement[ 4 ]
			unPersonnel[ 'nomService' ] = unEnregistrement[ 5 ]
			personnels.append( unPersonnel )
			
		curseur.close()
		return personnels
		
	except :
		return None
		
def activerCarte( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set activee = 1
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
	
	except :
		return None
	
def bloquerCarte( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set activee = 0
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None
		

def crediterCarte(numeroCarte, somme):
    try:
        curseur = getConnexionBD().cursor()

        requete = '''
            update Carte
            set solde = solde + %s
            where numeroCarte = %s
            '''

        curseur.execute(requete, (somme, numeroCarte))
        connexionBD.commit()
        nbTuplesTraites = curseur.rowcount
        curseur.close()

        return nbTuplesTraites

    except:
        return None
        
def debiterCarte(numeroCarte, somme):
    try:
        curseur = getConnexionBD().cursor()

        requete = '''
            update Carte
            set solde = solde - %s
            where numeroCarte = %s
            '''

        curseur.execute(requete, (somme, numeroCarte))
        connexionBD.commit()
        nbTuplesTraites = curseur.rowcount
        curseur.close()

        return nbTuplesTraites

    except:
        return None



def reinitialiserMdp(numeroCarte):
    try:
        curseur = getConnexionBD().cursor()
        
        requete = '''
            UPDATE Carte
            SET mdpCarte = 'azerty'
            WHERE numeroCarte = %s
            '''
            
        curseur.execute(requete, (numeroCarte,))
        connexionBD.commit()
        nbTuplesTraites = curseur.rowcount
        curseur.close()
        
        return nbTuplesTraites
        
    except Exception as e:
        print("Une erreur s'est produite :", str(e))
        return None



def modifierMdpUsager( numeroCarte , nouveauMdp) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set mdpCarte = %s
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( nouveauMdp , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None


def creerCarte(solde, matricule, activee):
    try:
        curseur = getConnexionBD().cursor()
        
        requete = '''
            INSERT INTO Carte (solde, dateCreation, activee, matricule)
            VALUES (%s, CURRENT_DATE(), %s, %s)
        '''
            
        curseur.execute(requete, (solde, activee, matricule))
        connexionBD.commit()
        nbTuplesTraites = curseur.rowcount
        curseur.close()
        
        return nbTuplesTraites
        
    except mysql.connector.Error as err:
        print("Erreur MySQL : {}".format(err))
        return None




def enregistrerReservation( numeroCarte , dateReservation ):
	try:
		curseur = getConnexionBD().cursor()

		requete = '''
			insert into Reservation( dateResa , numeroCarte )
			values( %s , %s )
			'''

		curseur.execute(requete, ( dateReservation , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()

		return nbTuplesTraites

	except:
		return None


def annulerReservation( numeroCarte , dateReservation ):
	try:
		curseur = getConnexionBD().cursor()

		requete = '''
			delete from Reservation
			where numeroCarte = %s
			and dateResa = %s
			'''

		curseur.execute(requete, ( numeroCarte , dateReservation ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()

		return nbTuplesTraites

	except:
		return None


def get_reservations_par_carte( numeroCarte , dateDebut , dateFin ):
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select dateResa
					from Reservation
					where numeroCarte = %s
					and dateResa >= %s
					and dateResa <= %s 
				'''

		curseur.execute(requete, ( numeroCarte , dateDebut , dateFin ) )

		enregistrements = curseur.fetchall()

		dates = []
		for unEnregistrement in enregistrements:
			
			uneDate = '%04d-%02d-%02d' % ( unEnregistrement[0].year , unEnregistrement[0].month , unEnregistrement[0].day )
			
			dates.append( uneDate )

		curseur.close()
		return dates

	except:
		return None


def getHistoriqueReservationsCarte( numeroCarte ) :
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select dateResa
					from Reservation
					where numeroCarte = %s
					order by dateResa DESC
				'''

		curseur.execute(requete, ( numeroCarte , ) )

		enregistrements = curseur.fetchall()

		dates = []
		for unEnregistrement in enregistrements:
			
			uneDate = '%04d-%02d-%02d' % ( unEnregistrement[0].year , unEnregistrement[0].month , unEnregistrement[0].day )
			
			dates.append( uneDate )

		curseur.close()
		return dates

	except:
		return None

	
def get_reservations_par_date( date_resa_str ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select Carte.numeroCarte
					from Reservation
					inner join Carte
					on Carte.numeroCarte = Reservation.numeroCarte
					where Reservation.dateResa = %s
				'''

		curseur.execute( requete , ( date_resa_str , ) )
		
		enregistrements = curseur.fetchall()
		
		reservations = []
		for unEnregistrement in enregistrements :
			uneReservation = {}
			uneReservation[ 'numeroCarte' ] = unEnregistrement[ 0 ]
			reservations.append( uneReservation )
			
		curseur.close()
		return reservations
		
	except :
		return None

	
def debiterSolde( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set solde = solde - (
				select tarifRepas
				from Fonction
				inner join Personnel
				on Personnel.idFonction = Fonction.idFonction
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites

	except :
		return None
		
	
def crediterSolde( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set solde = solde + (
				select tarifRepas
				from Fonction
				inner join Personnel
				on Personnel.idFonction = Fonction.idFonction
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites

	except :
		return None
	
def historique_reservations(matricule):
    reservations = None
    try:
        curseur = getConnexionBD().cursor()
        query_carte = '''
            SELECT dateResa
            FROM Reservation
            INNER JOIN Carte ON Reservation.numeroCarte = Carte.numeroCarte
            WHERE Carte.matricule = %s
            ORDER BY dateResa DESC
        '''
        curseur.execute(query_carte, (matricule,))
        reservations = curseur.fetchall()
        curseur.close()
    except mysql.connector.Error as e:
        print("Erreur lors de la récupération de l'historique des réservations :", e)
        reservations = None
    return reservations			
		
if __name__=="__main__":
	print(seConnecterUsager(1,"azerty"))
	
	
