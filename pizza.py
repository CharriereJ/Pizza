# Application web gérant des commandes de pizzas

import os, cherrypy

class SitePizza(object):
    "Classe produisant des objets gestionnaires de requetes HTTP"

    def __init__(self):
        "Définition d'attributs propres à l'application"

        self.count = 0 # compteur de commandes
            

    def index(self):
        # Cherrypy invoquera cette méthode comme URL racine du site.
        # Sa valeur de retour sera la page web contenant le formulaire
        # de commande de pizzas dont le code HTML est situé dans un fichier externe.

        fichier = open('annexes/templates/formulaire.html', 'r', encoding='utf8')
        code = fichier.read()
        return code

    index.exposed = True

    def commande(self, garniture1, garniture2, garniture3, taille, nom=None, adresse=None):
        # Cherrypy passe les valeurs entrées dans un formulaire comme de simples
        # arguments lors de l'appel de la méthode gestionnaire de la requete.

        if nom and adresse:

            # Augmentation du compteur de commandes:
            self.count += 1

            # Ticket de validation pour la pizzeria:
            nomFichier = 'annexes/commandes/commande'+str(self.count)+'.txt'
            ticket = open(nomFichier, 'w', encoding='utf8')
            commande = "Une pizza {size} avec {gar1}, {gar2}, {gar3} a été commandée par {client} à l'adresse {lieu}".\
                       format(size=taille, gar1=garniture1, gar2=garniture2, gar3=garniture3, client=nom, lieu=adresse)
            ticket.write(commande)
            ticket.close()

            # Création du fichier HTML à retourner au client:
            reponse = open('annexes/templates/reponse.html', 'r', encoding='utf8')
            code = reponse.read().format(gar1=garniture1, gar2=garniture2,\
                                         gar3=garniture3, size=taille, client=nom,\
                                         lieu=adresse, compteur = self.count)
            return code

        else:
            erreur = open('annexes/templates/erreur.html', 'r', encoding='utf8')
            code = erreur.read()
            return code

    commande.exposed = True


# === PROGRAMME PRINCIPAL ====

# Reconfiguration du serveur Web (assure que le répertoire racine du
# site est bien le répertoire courant dans lequel est située
# l'application)
cherrypy.config.update({"tools.staticdir.root":os.getcwd()})

# Démarrage du serveur web :
cherrypy.quickstart(SitePizza(), config='tutoriel.conf')
