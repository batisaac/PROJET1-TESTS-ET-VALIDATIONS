# Intro
```
Hey,

Je viens de recevoir le rapport de QA pour la phase 1 du projet. Il y a plusieurs bogues, dont un qui fait planter l'application ! 
Malheureusement, je ne suis pas au bureau pour les prochains jours (un de mes enfants est tombé malade ce week-end). 
Je ne sais pas encore quand je pourrai être là dans la semaine. Pourriez-vous prendre en charge la mise en œuvre du projet ? 
Vous devrez régler les bogues de la phase 1 et mettre en œuvre les éléments de la phase 2 (j'ai ajouté le travail de la phase 2 et les bogues de la section “issues” du repo). 

Vous devrez cloner et forker le repo et le mettre en place sur votre machine locale (tout ce dont vous avez besoin se trouve dans le fichier README). 
Ensuite, passez en revue les bogues dans la section des problèmes, puis essayez de reproduire les problèmes sur votre machine locale pour résoudre les bogues et ajouter la gestion des erreurs. 
Pour gagner du temps de configuration, nous utilisons Flask et JSON pour éviter d'utiliser une base de données. 
La plupart des outils dont vous aurez besoin se trouvent dans le fichier requirements.txt dans le repo, 
mais vous devrez installer Flask et notre framework de test préféré, pytest, ainsi que notre outil de test de performance, Locust. 

Vous devrez également préparer un rapport de test et un rapport de performances, 
conformément au guide de développement à la fin des spécifications fonctionnelles ci-jointes. 
Veillez à suivre toutes les directives, car le QA nous reproche de ne pas respecter les normes. 
Vous devez tester de manière approfondie les résultats requis (à la fois les happy paths et les sad paths) pour toutes les fonctionnalités de l'application.  
Je vous encourage également à adopter une approche de TDD, car cela vous aidera à rationaliser votre travail. 

Une fois que vous aurez terminé, nous ferons un examen de ce que vous avez dans la branche QA du code. 
Nous examinerons les rapports et la manière dont vous avez résolu les problèmes, 
nous examinerons votre code et nous testerons la couverture de la nouvelle fonctionnalité. 

Merci !

```
1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

    We also like to show how well we're testing, so there's a module called 
    [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.

    Commandes (Windows, environnement `.venv`) :

    ```cmd
    .\.venv\Scripts\python.exe -m pytest -v
    .\.venv\Scripts\python.exe -m pytest --cov=server --cov=repository --cov=club --cov=competition --cov=config --cov=booking --cov-report=term-missing --cov-report=html
    ```

    Les tests sont séparés en trois niveaux :

    | Dossier | Contenu |
    |---|---|
    | `test/unit/` | fonctions pures (`booking`, `club`, `competition`, `config`, `repository`) |
    | `test/integration/` | routes Flask avec le client de test |
    | `test/fonctionnel/` | parcours complets de bout en bout |

    Résultat actuel : **70 tests verts**, couverture applicative **100 %**.
    Le test de charge Locust est décrit plus bas.

 6. Flake8 Report 
    
    Commande : `flake8 .` (configuration dans `setup.cfg`, environnement `.venv` exclu)

    ```
    (aucune sortie)
    ```

    Résultat : **0 erreur**.

7. Documentation et liens

    - Rapport de test : [`rapport-de-test.md`](rapport-de-test.md)
    - Rapport de performances : [`rapport-de-performances.md`](rapport-de-performances.md)
    - Dépôt : <https://github.com/batisaac/PROJET1-TESTS-ET-VALIDATIONS>
    - [Flask](https://flask.palletsprojects.com/), [pytest](https://docs.pytest.org/),
      [pytest-cov](https://pytest-cov.readthedocs.io/), [Locust](https://docs.locust.io/),
      [Flake8](https://flake8.pycqa.org/)

    Le rapport de test contient l'inventaire des anomalies (B1 à B24), leur reproduction,
    les tests associés (T-U, T-I, T-F), la couverture, Flake8 et les limites connues.
    Le rapport de performances contient le protocole Locust et les mesures.

8. Configuration

    | Élément | Valeur |
    |---|---|
    | Python | 3.14 |
    | Flask | 3.1.3 |
    | pytest / pytest-cov | 9.1.1 / 7.1.0 |
    | Flake8 | 7.4.1 (limite 99, `.venv` exclu) |
    | Locust | 2.47.0 |

    - Installer les dépendances : `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
    - Lancer le serveur : `.\.venv\Scripts\python.exe -m flask --app server run`
    - Clé de session : variable d'environnement `SECRET_KEY`. Si elle est absente, une clé
      aléatoire est générée au démarrage (les sessions sont alors perdues au redémarrage).
    - Données : `clubs.json` et `competitions.json`, réécrits après chaque achat.
    - Test de charge :

      ```cmd
      .\.venv\Scripts\python.exe -m flask --app server run --port 5011
      .\.venv\Scripts\locust.exe -f locustfile.py --headless -u 6 -r 6 -t 30s --host http://127.0.0.1:5011
      git checkout -- clubs.json competitions.json
      ```

      La dernière commande restaure les données, car les achats simulés les modifient.

9. Conventions de développement

    - Une branche par anomalie ou fonctionnalité : `<type>/<nom-descriptif>`
      (`bug/`, `refactor/`, `chore/`, `feature/`, `test/`, `perf/`, `docs/`).
    - TDD : écrire le test (rouge), écrire le minimum de code (vert), puis refactorer.
    - Commits : `type: description (Bxx)` quand un identifiant d'anomalie existe.
    - `main` reste la source de vérité ; chaque branche est poussée puis fusionnée en
      avance rapide (`git merge --ff-only`).
    - La branche `QA` est créée depuis `main` en fin de projet et **n'est jamais fusionnée**.
    - Logique métier dans des fonctions pures (`booking.py`, `club.py`, `competition.py`,
      `repository.py`) ; les routes appliquent les effets de bord.
    - Tests nommés en français, identifiants T-U (unitaire), T-I (intégration),
      T-F (fonctionnel).

10. FAQ

    **Pourquoi le tableau de bord est-il vide après connexion ?**
    Les compétitions fournies sont datées de 2020. L'application n'affiche que les
    compétitions à venir (exigence B23) ; mettez une date future dans `competitions.json`
    pour les voir.

    **Pourquoi un achat est-il refusé ?**
    Cinq règles sont vérifiées dans cet ordre : quantité ≥ 1, concours complet, stock
    suffisant, maximum 12 places par achat, solde de points suffisant. Le message affiché
    indique la règle concernée.

    **Pourquoi « Sorry, you must be logged in. » ?**
    `/book` et `/purchasePlaces` exigent une session ouverte via `/showSummary`, et le club
    du formulaire doit être celui de la session.

    **Comment restaurer les données d'origine ?**
    `git checkout -- clubs.json competitions.json`.

    **Pourquoi ne pas lancer deux `pytest` en parallèle ?**
    Les tests de persistance écrivent dans les vrais fichiers JSON, restaurés par la fixture.
    Deux exécutions simultanées se marcheraient dessus.

    **Où sont les preuves ?**
    `rapport-de-test.md`, `rapport-de-performances.md`, `reproduction_bugs.py` et l'historique
    Git (une branche par anomalie).


