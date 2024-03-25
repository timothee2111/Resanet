#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import *
from modeles import modeleResanet
from technique import datesResanet


app = Flask( __name__ )
app.secret_key = 'resanet'





@app.route( '/' , methods = [ 'GET' ] )
def index() :
	return render_template( 'vueAccueil.html' )

@app.route( '/usager/session/choisir' , methods = [ 'GET' ] )
def choisirSessionUsager() :
	return render_template( 'vueConnexionUsager.html' , carteBloquee = False , echecConnexion = False , saisieIncomplete = False )

@app.route( '/usager/seConnecter' , methods = [ 'POST' ] )
def seConnecterUsager() :
	numeroCarte = request.form[ 'numeroCarte' ]
	mdp = request.form[ 'mdp' ]

	if numeroCarte != '' and mdp != '' :
		usager = modeleResanet.seConnecterUsager( numeroCarte , mdp )
		if len(usager) != 0 :
			if usager[ 'activee' ] == True :
				session[ 'numeroCarte' ] = usager[ 'numeroCarte' ]
				session[ 'nom' ] = usager[ 'nom' ]
				session[ 'prenom' ] = usager[ 'prenom' ]
				session[ 'mdp' ] = mdp
				
				return redirect( '/usager/reservations/lister' )
				
			else :
				return render_template('vueConnexionUsager.html', carteBloquee = True , echecConnexion = False , saisieIncomplete = False )
		else :
			return render_template('vueConnexionUsager.html', carteBloquee = False , echecConnexion = True , saisieIncomplete = False )
	else :
		return render_template('vueConnexionUsager.html', carteBloquee = False , echecConnexion = False , saisieIncomplete = True)


@app.route( '/usager/seDeconnecter' , methods = [ 'GET' ] )
def seDeconnecterUsager() :
	session.pop( 'numeroCarte' , None )
	session.pop( 'nom' , None )
	session.pop( 'prenom' , None )
	return redirect( '/' )


@app.route( '/usager/reservations/lister' , methods = [ 'GET' ] )
def listerReservations() :
	tarifRepas = modeleResanet.getTarifRepas( session[ 'numeroCarte' ] )
	
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	
	solde = '%.2f' % ( soldeCarte , )

	aujourdhui = datesResanet.getDateAujourdhuiISO()

	datesPeriodeISO = datesResanet.getDatesPeriodeCouranteISO()
	
	datesResas = modeleResanet.getReservationsCarte( session[ 'numeroCarte' ] , datesPeriodeISO[ 0 ] , datesPeriodeISO[ -1 ] )
	
	dates = []
	for uneDateISO in datesPeriodeISO :
		uneDate = {}
		uneDate[ 'iso' ] = uneDateISO
		uneDate[ 'fr' ] = datesResanet.convertirDateISOversFR( uneDateISO )
		
		if uneDateISO <= aujourdhui :
			uneDate[ 'verrouillee' ] = True
		else :
			uneDate[ 'verrouillee' ] = False

		if uneDateISO in datesResas :
			uneDate[ 'reservee' ] = True
		else :
			uneDate[ 'reservee' ] = False
			
		if soldeCarte < tarifRepas and uneDate[ 'reservee' ] == False :
			uneDate[ 'verrouillee' ] = True
			
			
		dates.append( uneDate )
	
	if soldeCarte < tarifRepas :
		soldeInsuffisant = True
	else :
		soldeInsuffisant = False
		
	jour = ["lundi","mardi","mercredi","jeudi","vendredi"]
	return render_template( 'vueListeReservations.html' , dayName = jour,laSession = session , leSolde = solde , lesDates = dates , soldeInsuffisant = soldeInsuffisant )

	
@app.route( '/usager/reservations/annuler/<dateISO>' , methods = [ 'GET' ] )
def annulerReservation( dateISO ) :
	modeleResanet.annulerReservation( session[ 'numeroCarte' ] , dateISO )
	modeleResanet.crediterSolde( session[ 'numeroCarte' ] )
	return redirect( '/usager/reservations/lister' )
	
@app.route( '/usager/reservations/enregistrer/<dateISO>' , methods = [ 'GET' ] )
def enregistrerReservation( dateISO ) :
	modeleResanet.enregistrerReservation( session[ 'numeroCarte' ] , dateISO )
	modeleResanet.debiterSolde( session[ 'numeroCarte' ] )
	return redirect( '/usager/reservations/lister' )

@app.route( '/usager/mdp/modification/choisir' , methods = [ 'GET' ] )
def choisirModifierMdpUsager() :
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	solde = '%.2f' % ( soldeCarte , )
	
	return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = '' )

@app.route( '/usager/mdp/modification/appliquer' , methods = [ 'POST' ] )
def modifierMdpUsager() :
	ancienMdp = request.form[ 'ancienMDP' ]
	nouveauMdp = request.form[ 'nouveauMDP' ]
	
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	solde = '%.2f' % ( soldeCarte , )
	
	if ancienMdp != session[ 'mdp' ] or nouveauMdp == '' :
		return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = 'Nok' )
		
	else :
		modeleResanet.modifierMdpUsager( session[ 'numeroCarte' ] , nouveauMdp )
		session[ 'mdp' ] = nouveauMdp
		return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = 'Ok' )


@app.route( '/gestionnaire/session/choisir' , methods = [ 'GET' ] )
def choisirSessionGestionnaire() :
	return render_template( 'vueConnexionGestionaire.html' ,echecConnexion = False , saisieIncomplete = False )

@app.route( '/gestionnaire/seConnecter' , methods = [ 'POST' ] )
def seConnecterGestionnaire() :
	login = request.form[ 'login' ]
	mdp = request.form[ 'mdp' ]

	if login != '' and mdp != '' :
		gestionnaire = modeleResanet.seConnecterGestionnaire( login , mdp )
		if gestionnaire is not None:
			session[ 'login' ] = gestionnaire[ 'login' ]
			session[ 'nom' ] = gestionnaire[ 'nom' ]
			session[ 'prenom' ] = gestionnaire[ 'prenom' ]
			session[ 'mdp' ] = gestionnaire
			
			return redirect( '/gestionnaire/Personnel/AvecCarte' )
				
		else :
			return render_template('vueConnexionGestionaire.html',  echecConnexion = True , saisieIncomplete = False )
	else :
		return render_template('vueConnexionGestionaire.html', echecConnexion = False , saisieIncomplete = True)

@app.route('/gestionnaire/Personnel/SansCarte' , methods = ['GET'])
def personelSansCarte() : 
	persoSansCarte = modeleResanet.getPersonnelsSansCarte()
	return render_template( 'vuePersonnelSansCarte.html' , SansCarte = persoSansCarte)

@app.route('/gestionnaire/Personnel/SansCarte/CréerCarte' , methods = ['GET'])
def créerCarte() : 
	return render_template( 'vueCréerCarte.html')

@app.route('/gestionnaire/Personnel/AvecCarte' , methods = ['GET'])
def personelAvecCarte() : 
	persoAvecCarte = modeleResanet.getPersonnelsAvecCarte()
	return render_template( 'vuePersonnelAvecCarte.html' , avecCarte = persoAvecCarte)

@app.route('/gestionnaire/Personnel/AvecCarte/bloquer/<numeroCarte>', methods = ['GET'])
def bloquerCarte(numeroCarte):
	modeleResanet.bloquerCarte(numeroCarte)
	return redirect('/gestionnaire/Personnel/AvecCarte')
	
@app.route('/gestionnaire/Personnel/AvecCarte/activer/<numeroCarte>', methods = ['GET'])
def activerCarte(numeroCarte):
	modeleResanet.activerCarte(numeroCarte)
	return redirect('/gestionnaire/Personnel/AvecCarte')
	
@app.route('/gestionnaire/Personnel/AvecCarte/reinitialiser/<numeroCarte>', methods = ['GET'])
def reinitialiserMdp(numeroCarte):
	modeleResanet.reinitialiserMdp(numeroCarte)
	return redirect('/gestionnaire/Personnel/AvecCarte')
	
	
@app.route('/gestionnaire/Personnel/AvecCarte/crediter/somme/<numeroCarte>' , methods = ['GET'])
def debit(numeroCarte):
	return render_template('vueCrediterCarte.html', numeroCarte = numeroCarte)
	
@app.route('/gestionnaire/Personnel/AvecCarte/debiter/somme/<numeroCarte>' , methods = ['GET'])
def credit(numeroCarte):
	return render_template('vueDebiterCarte.html', numeroCarte = numeroCarte)
	
	
@app.route('/gestionnaire/Personnel/AvecCarte/crediter/<numeroCarte>' , methods = ['POST'])
def crediterCarte(numeroCarte):
    somme = request.form.get('somme')
    if somme is not None and somme.isdigit():
        modeleResanet.crediterCarte(numeroCarte, int(somme))
        return redirect('/gestionnaire/Personnel/AvecCarte')
    else:
        return "Erreur : Somme invalide."
        
@app.route('/gestionnaire/Personnel/AvecCarte/debiter/<numeroCarte>' , methods = ['POST'])
def debiterCarte(numeroCarte):
    somme = request.form.get('somme')
    if somme is not None and somme.isdigit():
        modeleResanet.debiterCarte(numeroCarte, int(somme))
        return redirect('/gestionnaire/Personnel/AvecCarte')
    else:
        return "Erreur : Somme invalide."
	
	
@app.route('/gestionnaire/Carte/Créer/', methods=['POST'])
def creerCarte():
	
    solde = request.form['solde']
    matricule = request.form['matricule']
    activee = request.form['activee']

    activee = True if activee == 'true' else False

    success = modeleResanet.creerCarte(solde, matricule, activee)

    return redirect('/gestionnaire/Personnel/AvecCarte')
        		
	
@app.route('/gestionnaire/Resa/Date/Form', methods=['GET'])
def resa_date():
    return render_template('vueResaDate.html')
    
from datetime import datetime

@app.route('/gestionnaire/Reservations/date', methods=['POST'])
def afficher_reservations_par_date():
	date_resa_str = request.form.get('date_resa')
	date_resa = datetime.strptime(date_resa_str, '%Y-%m-%d').date()
	reservations = modeleResanet.get_reservations_par_date(date_resa_str)
	return render_template('vueReservationsParDate.html', reservations=reservations)


@app.route('/gestionnaire/Resa/Carte/Form' , methods = ['GET'])
def ResaCarte():
	return render_template('vueResaCarte.html')
	
@app.route('/gestionnaire/Reservations/carte', methods=['POST'])
def afficher_reservations_par_carte():
	numeroCarte = request.form.get('carte_resa')
	reservations = modeleResanet.getHistoriqueReservationsCarte(numeroCarte)
	return render_template('vueReservationsParCarte.html', reservations=reservations)
	
	
@app.route('/historique/<int:matricule>')
def historique(matricule):
    reservations = modeleResanet.historique_reservations(matricule)
    return render_template('historique_reservations.html', reservations=reservations)
        
	
if __name__ == '__main__' :
	app.run( debug = True , host = '0.0.0.0' , port = 5000 )
