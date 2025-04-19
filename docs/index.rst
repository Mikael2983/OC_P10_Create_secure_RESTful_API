.. SoftDesk Support API documentation master file, created by
   sphinx-quickstart on Fri Apr 18 13:59:27 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SoftDesk Support API Documentation
==================================

Bienvenue sur la documentation officielle de l'API RESTful SoftDesk Support.

Ce projet propose une API sécurisée permettant de :

* gérer des projets logiciels collaboratifs
* suivre des tickets (issues)
* commenter les tâches
* gérer des contributeurs via un système d’autorisation

.. contents::
   :local:
   :depth: 2

Authentification
----------------

Inscription d’un nouvel utilisateur
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /users/register/

Inscrit un nouvel utilisateur.

**Corps de la requête :**

.. code-block:: json

   {
     "username": "john_doe",
     "password": "MotDePasse123!",
     "email": "john@example.com",
     "birth_date": "2000-01-01",
     "can_be_contacted": true,
     "can_data_be_shared": false
   }

**Contraintes :**
* L'utilisateur doit avoir au moins 15 ans
* L'email doit être unique
* Le mot de passe est hashé automatiquement

---

Obtenir un token JWT
^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /token/

Permet à un utilisateur de récupérer un token d’accès JWT.

**Corps de la requête :**

.. code-block:: json

   {
     "username": "john_doe",
     "password": "MotDePasse123!"
   }

**Contraintes :**
* Les identifiants doivent être valides

---

Rafraîchir un token JWT
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /token/refresh/

Permet de renouveler un token d'accès JWT.

**Corps de la requête :**

.. code-block:: json

   {
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
   }

**Contraintes :**
* Le token doit être encore valide

---

Utilisateurs
------------

Lister les utilisateurs
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /users/

Renvoie une liste des utilisateurs publics (username uniquement).

---

Voir son propre profil
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /users/{id}/

Renvoie les informations du profil connecté.

**Contraintes :**
* Le profil des autres utilisateurs n’est pas accessible

---

Projets
-------

Lister les projets
^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /projects/

Liste les projets visibles par l’utilisateur connecté (s’il est contributeur).

---

Créer un projet
^^^^^^^^^^^^^^^

.. code-block:: http

   POST /projects/

Crée un nouveau projet.

**Corps de la requête :**

.. code-block:: json

   {
     "title": "Nom du projet",
     "description": "Description du projet",
     "type": "back-end",
     "contributors_ids": [2, 3]
   }

**Contraintes :**
* L’auteur est automatiquement ajouté comme contributeur
* `contributors_ids` ne fonctionne que lors de la création

---

Voir un projet
^^^^^^^^^^^^^^

.. code-block:: http

   GET /projects/{id}/

Renvoie les détails du projet.

---

Modifier un projet
^^^^^^^^^^^^^^^^^^

.. code-block:: http

   PATCH /projects/{id}/

Permet de modifier un projet existant.

**Corps de la requête (exemple partiel) :**

.. code-block:: json

   {
     "title": "Nouveau titre",
     "description": "Nouvelle description",
     "type": "iOS"
   }

**Contraintes :**
* Seul l’auteur du projet peut le modifier
* `contributors_ids` non pris en charge ici

---

Supprimer un projet
^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   DELETE /projects/{id}/

Supprime le projet.

**Contraintes :**
* Seul l’auteur peut supprimer un projet

---

Ajouter un contributeur
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /projects/{id}/add_contributor/

Ajoute un contributeur à un projet.

**Corps de la requête :**

.. code-block:: json

   {
     "user_id": 4
   }

**Contraintes :**
* Seul l’auteur du projet peut ajouter un contributeur

---

Supprimer un contributeur
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   DELETE /projects/{id}/del_contributor/

Retire un contributeur du projet.

**Corps de la requête :**

.. code-block:: json

   {
     "user_id": 4
   }

**Contraintes :**
* Seul l’auteur peut retirer un contributeur
* L’auteur ne peut pas se retirer lui-même

---

Issues (Tâches)
---------------

Lister les issues
^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /issues/

Liste toutes les issues des projets où l’utilisateur est contributeur.

---

Créer une issue
^^^^^^^^^^^^^^^

.. code-block:: http

   POST /issues/

Crée une nouvelle issue liée à un projet.

**Corps de la requête :**

.. code-block:: json

   {
     "title": "Bug sur le formulaire",
     "description": "Le bouton submit plante",
     "priority": "High",
     "status": "To Do",
     "nature": "Bug",
     "assigned": 3,
     "project": 1
   }

**Contraintes :**
* `title` doit être unique dans un projet
* `assigned` doit être contributeur du projet
* `author` est automatiquement défini
* `project` doit être accessible
* `date_created` est ajouté automatiquement

---

Voir une issue
^^^^^^^^^^^^^^

.. code-block:: http

   GET /issues/{id}/

Renvoie les détails d'une issue.

---

Modifier ou supprimer une issue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   PATCH /issues/{id}/
   DELETE /issues/{id}/

Permet de modifier ou supprimer une issue.

**Contraintes :**
* Seul l’auteur de l’issue peut la modifier ou la supprimer

---

Commentaires
------------

Lister les commentaires
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /comments/

Liste les commentaires liés aux issues des projets du user.

---

Créer un commentaire
^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /comments/

Ajoute un commentaire à une issue.

**Corps de la requête :**

.. code-block:: json

   {
     "description": "Je m’en occupe",
     "issue": 5
   }

**Contraintes :**
* L’auteur est automatiquement défini
* Le projet lié à l’issue doit être accessible
* La date de création est ajoutée automatiquement

---

Voir un commentaire
^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /comments/{id}/

Affiche un commentaire.

---

Modifier ou supprimer un commentaire
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   PATCH /comments/{id}/
   DELETE /comments/{id}/

**Contraintes :**
* Seul l’auteur du commentaire peut le modifier ou le supprimer
