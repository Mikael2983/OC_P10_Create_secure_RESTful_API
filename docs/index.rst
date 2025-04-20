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

   POST /api/v1/users/register/

Inscrit un nouvel utilisateur.

**Champs requis :**

* ``username`` : *string* — identifiant unique
* ``password`` : *string* — mot de passe sécurisé
* ``birth_date`` : *string (date)* — format YYYY-MM-DD

**Champs optionnels :**

* ``can_be_contacted`` : *boolean*, par défaut => True
* ``can_data_be_shared`` : *boolean*, par défaut => True
* ``email`` : *string* — adresse email valide,  par défaut => Null

**Exemple de requête :**

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

* Le nom de l'utilisateur doit être unique
* L'utilisateur doit avoir au moins 15 ans
* L'email doit être unique

**Notes :**

* Le mot de passe est hashé automatiquement

---

Obtenir un token JWT
^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /api/v1/token/

Permet à un utilisateur de récupérer un token d’accès JWT.

**Champs requis :**

* ``username`` : *string*
* ``password`` : *string*

**Exemple :**

.. code-block:: json

    {
        "username": "john_doe",
        "password": "MotDePasse123!"
    }

**Réponse :**

.. code-block:: json

    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eX...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eX..."
    }
---

Rafraîchir un token JWT
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /api/v1/token/refresh/

Permet de renouveler un token JWT.

**Champs requis :**

* ``refresh`` : *string* — token de rafraîchissement

**Exemple :**

.. code-block:: json

    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
    }

**Réponse :**

.. code-block:: json

    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eX..."
    }
---

Utilisateurs
------------

Lister les utilisateurs
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /api/v1/users/

Renvoie une liste des utilisateurs publics (champs id et username uniquement).

---

Voir son propre profil
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /api/v1/users/{id}/

Renvoie les informations du profil connecté.

**Contraintes :**

* Le profil des autres utilisateurs n’est pas accessible

---

Projets
-------

Lister les projets
^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /api/v1/projects/

Liste les projets visibles par l’utilisateur connecté (s’il est contributeur).

---

Créer un projet
^^^^^^^^^^^^^^^

.. code-block:: http

   POST /api/v1/projects/

Crée un nouveau projet.

**Champs requis :**

* ``title`` : *string*
* ``description`` : *string*
* ``type`` : *string* — ``back-end``, ``front-end``, ``iOS``, ``Android``
* ``contributors_ids`` : *array of integers* — identifiants des utilisateurs

**Exemple :**

.. code-block:: json

    {
        "title": "Nom du projet",
        "description": "Un super projet",
        "type": "front-end",
        "contributors_ids": [2, 3]
    }

**Contraintes :**

* L’auteur est automatiquement ajouté comme contributeur
* `contributors_ids` ne fonctionne que lors de la création

---

Voir un projet
^^^^^^^^^^^^^^

.. code-block:: http

   GET /api/v1/projects/{id}/

Renvoie les détails du projet.

---

Modifier un projet
^^^^^^^^^^^^^^^^^^

.. code-block:: http

   PATCH /api/v1/projects/{id}/

Permet de modifier un projet existant.

**Champs modifiables :**

* ``title`` : *string*
* ``description`` : *string*
* ``type`` : *string*

**Exemple :**

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

   DELETE /api/v1/projects/{id}/

Supprime un projet existant.

**Contraintes :**

* Seul l’auteur peut supprimer un projet

---

Ajouter un contributeur
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /api/v1/projects/{id}/add_contributor/

Ajoute un contributeur à un projet.

**Champs requis :**

* ``user_id`` : *integer*

**Exemple :**

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

   DELETE /api/v1/projects/{id}/del_contributor/

Retire un contributeur du projet.

**Champs requis :**

* ``user_id`` : *integer*

**Exemple :**

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

   GET /api/v1/issues/

Liste toutes les issues des projets où l’utilisateur est contributeur.

---

Créer une issue
^^^^^^^^^^^^^^^

.. code-block:: http

   POST /api/v1/issues/

Crée une nouvelle tâche.

**Champs requis :**

* ``title`` : *string*
* ``description`` : *string*
* ``priority`` : *string* — ``Low``, ``Medium``, ``High``
* ``status`` : *string* — ``To Do``, ``In Progress``, ``Finished``
* ``nature`` : *string* — ``Bug``, ``Feature``, ``Task``
* ``assigned`` : *integer*
* ``project`` : *integer*

**Exemple :**

.. code-block:: json

    {
        "title": "Erreur formulaire",
        "description": "Le bouton plante",
        "priority": "High",
        "status": "To Do",
        "nature": "Bug",
        "assigned": 3,
        "project": 1
    }

**Contraintes :**

* `title` unique par projet
* `assigned` doit être contributeur du projet
* `author` est ajouté automatiquement
* `project` doit être valide
* `date_created` est générée automatiquement

---

Voir une issue
^^^^^^^^^^^^^^

.. code-block:: http

   GET /api/v1/issues/{id}/

Affiche les détails d'une issue.

---

Modifier ou supprimer une issue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   PATCH /api/v1/issues/{id}/
   DELETE /api/v1/issues/{id}/

**Contraintes :**

* Seul l’auteur de l’issue peut la modifier ou la supprimer

---

Commentaires
------------

Lister les commentaires
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /api/v1/comments/

Liste tous les commentaires accessibles.

---

Créer un commentaire
^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   POST /api/v1/comments/

Crée un commentaire.

**Champs requis :**

* ``description`` : *string*
* ``issue`` : *integer*

**Exemple :**

.. code-block:: json

    {
        "description": "Je m'en occupe",
        "issue": 2
    }

**Contraintes :**

* L’auteur est défini automatiquement
* L’utilisateur doit être contributeur du projet lié à l’issue
* La date de création est ajoutée automatiquement

---

Voir un commentaire
^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   GET /api/v1/comments/{id}/

Affiche un commentaire.

**Note :** ``id`` est un identifiant au format *UUID*.

---

Modifier ou supprimer un commentaire
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: http

   PATCH /api/v1/comments/{id}/
   DELETE /api/v1/comments/{id}/

**Note :** ``id`` est un identifiant au format *UUID*.

**Contraintes :**

* Seul l’auteur du commentaire peut le modifier ou le supprimer