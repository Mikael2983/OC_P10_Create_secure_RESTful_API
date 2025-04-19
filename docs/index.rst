.. SoftDesk Support API documentation master file, created by
   sphinx-quickstart on Fri Apr 18 13:59:27 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SoftDesk Support API Documentation
=============================================

Ce projet propose une API sécurisée permettant de :

 * gérer des projets logiciels collaboratifs
 * suivre des tickets (issues)
 * commenter les tâches
 * gérer des contributeurs via un système d’autorisation

SoftDesk Support API Documentation
==================================

Bienvenue sur la documentation officielle de l'API RESTful SoftDesk Support.
Ce document décrit les endpoints disponibles, les méthodes HTTP autorisées, les paramètres requis, et les schémas JSON attendus.

----

Authentification
----------------

**POST** `/users/register/`
Inscrire un nouvel utilisateur.

Requête :
- `username`: string
- `password`: string
- `email`: string
- `birth_date`: string (date)
- `can_be_contacted`: boolean
- `can_data_be_shared`: boolean

**POST** `/token/`
Obtenir un token JWT.

Requête :
- `username`: string
- `password`: string

**POST** `/token/refresh/`
Rafraîchir un token JWT.

Requête :
- `refresh`: string

Utilisateurs
------------

**GET** `/users/`
Lister les utilisateurs publics (username uniquement).

**GET** `/users/{id}/`
Voir les détails de son profil.
le profil des autres utilisateurs n'est pas accessible.

----

Projets
-------

**GET** `/projects/`
Lister les projets visibles dont l'utilisateur est un contributeur.

**POST** `/projects/`
Créer un projet.

Requête :
- `title`: string
- `description`: string
- `type`: string (back-end, front-end, iOS, Android)
- `contributors_ids`: liste d'integer  (id d'utilisateur)

**GET** `/projects/{id}/`
Voir les détails d'un projet.

**DELETE** `/projects/{id}/`
supprimer un projet.

**PATCH** `/projects/{id}/`
modifier un projet.

Requête :
- `title`: string
- `description`: string
- `type`: string (back-end, front-end, iOS, Android)

le champs `contributors_ids` ne fonctionne que lors de la création du project.
Pour ajouter ou supprimer des contributeurs au projet, voir ci-dessous.
Seul l'auteur du projet peut ajouter ou retirer des contributeurs

**POST** `/projects/{id}/add_contributor/`
Ajouter un contributeur.

Requête :
- `user_id`: integer

**DELETE** `/projects/{id}/del_contributor/`
Supprimer un contributeur.

Requête :
- `user_id`: integer

----

Issues (Tâches)
---------------

**GET** `/issues/`
Lister toutes les issues des projets dont l'utilisateur est contributeur.

**POST** `/issues/`
Créer une issue.

Requête :
- `title`: string
- `description`: string
- `priority`: Low / Medium / High
- `status`: To Do / In Progress / Finished
- `nature`: Bug / Feature / Task
- `assigned`: integer (id de l’utilisateur)
- `project`: integer (id du projet)

Contraintes :
- `title`: deux issues d'un même projet ne peuvent pas avoir le même titre
- `assigned`: l'utilisateur doit être contributeur du projet
- `project`: l'auteur de l'issue doit être contributeur du projet
- `author`: l'utilisateur connecté est ajouté automatiquement
- `date_created`: la date de creation est ajoutée

**GET** `/issues/{id}/`
Voir les détails d'une issue.

**PATCH / DELETE** `/issues/{id}/`
modifier ou supprimer une issue.

Contraintes:
seul l'auteur peut modifier ou supprimer une issue

----

Commentaires
------------

**GET** `/comments/`
Lister tous les commentaires des issues, des projets dont l'utilisateur est contributeur.

**POST** `/comments/`
Créer un commentaire.

Requête :
- `description`: string
- `issue`: integer (id de l’issue)

Contraintes:
- `issue`: l'auteur doit être contributeur du project lié à l'issue
- `author`: l'utilisateur connecté est ajouté automatiquement
- `date_created`: la date de creation est ajoutée automatiquement

**GET** `/comments/{id}/`
Voir, modifier ou supprimer un commentaire.

**PATCH / DELETE** `/comments/{id}/`
modifier ou supprimer un commentaire.

Contraintes:
seul l'auteur peut modifier ou supprimer un commentaire

----

