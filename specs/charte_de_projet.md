# Charte de Projet


| Nom   | Responsable | Date de modification
| -------- | ------- | -------- |
| PP2I1  | E. MANDJUKOWSKI  |  2024-09-01 |


### Buts et objectifs 

- Mise en place d'une plateforme web permettant au plus grand nombre de participer dans une moindre mesure à la lutte contre le réchauffement climatique.
- Encourager à réduire la production de déchets.

### Cadrage

###  Contexte

La crise écologique est une crise qui touche tout le monde, et nous avons tous un rôle à jouer. Par an, la production de déchets mondiale est d'environ 2.01 milliards de tonnes. Pour cela, les différents Etats ont opté pour une solution globalement similaire : des camions de ramassage de poubelles. Pour autant, les besoins ne sont pas les mêmes : on ne génère pas tous autant de déchets, à la même vitesse, ou parfois, on n'en produit même pas : c'est le cas lorsqu'on est en vacances par exemple. Or, les camions de ramasssage, eux, vont quand même effectuer un trajet et vider la poubelle. Une poubelle qui sera, de fait, déjà vide.

Notre solution numérique permet donc plusieurs choses : 
- organiser un ramassage des poubelles qui en ont *vraiment* besoin. Toutes les poubelles n'ayant pas la même taille, elles n'ont pas toutes besoin d'être vidées toutes les semaines.
- Organiser des trajets optimaux pour nos camions : que les camions soient électriques ou aux énergies fossiles, ils polluent lorsqu'ils roulent. S'ils roulent moins, ils pollueront donc moins.


### Finalité

- Accompagner chacun dans la gestion des déchets qu'il produit.
- Permettre à tous de se rendre compte combien de nous produisons, afin d'inciter encore plus à réduire notre production de déchets.

### Business Case

- Offrir une solution certes plus chère que celle proposée par la mairie, mais aussi plus écologique : les gens sont prêts à payer plus pour se battre pour des idéaux qui leur tiennent à coeur.

### Livrables attendus

- Un site internet complet, avec un système de connexion pour chaque utilisateur, un magasin, une page de profil propre aux utilisateurs, et une page administrateur afin de gérer la plateforme.

### Livrables

Les livrables contiennent les éléments suivants :

- Un serveur web permettant l'accès à la plateforme web et permettant des échanges
avec une base de données.

* Une base de données avec des informations sur les clients, les produits accessibles dans le magasin, les ramassages effectués, les poubelles déjà mises en places, les camions de ramassage.


### Critères de validation

Les critères de validation sont les suivants :

- Au minimum :
    - L'application web est fonctionnelle : système de comptes utilisateurs, boutique en ligne, gestion côté administrateur (ajout de produits, lancer un ramassage, historique des achats)
    - Utilisable sur ordinateur, pas forcément sur téléphone portable (dépendant des pages)
    - Les trajets proposés par les algorithmes de recherches sont *corrects*, sans pour autant être exacts.

- De façon convenable :
    - Des articles concernant la gestion des déchets, la réduction de la production de déchets etc.
    - Affichage des poubelles côté utilisateur et administrateur sur une carte dynamique.
    - Un système de tickets.
    - Un système pour ajouter des produits dans le magasin, côté administrateur évidemment.
  
- Au mieux (si le temps le permet) :
  - Côté administrateur, un moyen d'écrire ces articles.
  - Un système de statistiques pour que chaque utilisateur voit plus précisément sa production, le volume recyclé, le volume récupéré chaque année, etc.
  - L'utilisateur peut décider de modifier son compte, voire le supprimer, de modifier son mot de passe, son nom, son prénom.


### Ressources

* **Ressources humaines** limitées à 4 personnes.
__Toutes les personnes n'ont pas forcément d'expérience dans la création d'application
web -> Risques et difficultés__

* **Deadline** fixée au 15/01/2024 à 00h.

### Organisation

* Par son expérience, E. MANDJUKOWSKI hérite de la responsabilité du projet.

* L'ensemble du projet sera disponible sur GitHub, [ici](https://github.com/Esteban795/PP2I1/tree/main).

* Les réunions auront lieu toutes les semaines, à jour variable selon les disponibilités. Les comptes rendus sont disponibles [ici](https://github.com/Esteban795/PP2I1/tree/main), dans le dossier `specs/gdp/Compte_Rendu`.
Les comptes-rendus seront disponibles sur GitHub, dans le dossier `specs/comptes-rendus`. 

* Les tâches et leurs répartitions seront disponibles sur GitHub, dans la matrice RACI (disponible dans `/specs/gdp/matrice_RACI.pdf`).

### Risques

* Difficultés de l'équipe à se motiver.
* Incompétences des membres.
* Mauvaise gestion des ressources.
* Mauvaise communication.
* Mauvais choix technologiques.
* Difficultés liées à des facteurs externes :
__ex: Module WEB tardif, et au final peu utile..__
* Le choix de Flask.
* Utilisation difficile de git, de respect de formats (messages de commits, merge requests etc).

### Opportunités

* Apprentissage pour presque tous les membres.
* Découverte du travail en équipe en projet informatique pour presque tous les membres.
