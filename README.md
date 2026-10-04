# Todo Django → test d'hébergement Wasmer Edge (MySQL)

Mini todo-list (ajouter / terminer / supprimer) + admin Django + page `/health/` de diagnostic.

## Lancer en local
```bash
python -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser      # optionnel (pour /admin/)
python manage.py runserver
```
Sans variable `DB_HOST`, le projet utilise SQLite. Pour tester avec un vrai MySQL local :
```bash
export DB_HOST=127.0.0.1 DB_PORT=3306 DB_NAME=todo DB_USERNAME=root DB_PASSWORD=secret
python manage.py migrate && python manage.py runserver
```

## Déployer sur Wasmer Edge
1. Pousse le projet sur GitHub (`manage.py` et `requirements.txt` à la racine du repo).
2. wasmer.io → **Apps → Import from Git** → choisis le repo.
3. Dans **Enable Database**, active-la et choisis **MySQL**.
4. Ajoute les variables / secrets : `SECRET_KEY` (valeur aléatoire longue).
   Pour voir les erreurs détaillées pendant les tests : `DEBUG=True` (à retirer ensuite).
5. Déploie, puis ouvre `https://<app>-<owner>.wasmer.app/health/`
   → attendu : `{"status": "ok", "db_vendor": "mysql", ...}`

Si les tables n'existent pas (erreur « Table ... doesn't exist »), les migrations
n'ont pas tourné : lance `python manage.py migrate` via une session distante / SSH
sur l'app (voir la doc Wasmer « Remote Sessions » / « App SSH »).

## Points d'attention déjà gérés dans ce projet
- `config/wsgi.py` expose une variable publique **`app`** (exigé par Wasmer) et `WSGI_APPLICATION = "config.wsgi.app"`.
- `ALLOWED_HOSTS` contient `.wasmer.app` ; `CSRF_TRUSTED_ORIGINS` contient `https://*.wasmer.app`.
- Base MySQL lue depuis `DB_HOST`, `DB_PORT` (≠ 3306 !), `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`.
- Driver **PyMySQL** (pur Python) au lieu de `mysqlclient` (compilation C, risquée sous WASIX).
- Statiques servis par WhiteNoise (admin inclus), sans étape `collectstatic` obligatoire.
