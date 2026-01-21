# APT-Erfolg Lernplattform

Dies ist eine webbasierte Lernplattform zur Vorbereitung auf die IHK-Abschlussprüfung Teil 1 (APT1). Die Software festigt theoretisches Wissen durch adaptive Wiederholung (Spaced Repetition) und erhält die Motivation durch Gamification-Elemente wie "Boss-Fights" aufrecht.

## Architektur

- **Backend:** Python mit dem FastAPI-Framework
- **Frontend:** Angular mit Angular Material
- **Datenbank:** MariaDB

---

## Installationsanleitung

### Voraussetzungen

- Python 3.9+ und pip
- Node.js 18+ und npm
- Docker und Docker Compose (für die Datenbank)

### 1. Backend einrichten

1.  **Navigieren Sie in das Backend-Verzeichnis:**
    ```bash
    cd backend
    ```

2.  **Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # Auf Windows: venv\Scripts\activate
    ```

3.  **Installieren Sie die Python-Abhängigkeiten:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Erstellen Sie eine `.env`-Datei:**
    Erstellen Sie eine Datei namens `.env` im `backend`-Verzeichnis und fügen Sie die folgenden Umgebungsvariablen hinzu. Passen Sie die Werte für Ihre lokale MariaDB-Instanz an.

    ```env
    DATABASE_USER=user
    DATABASE_PASSWORD=password
    DATABASE_HOST=mariadb
    DATABASE_NAME=apt_erfolg_db
    SECRET_KEY=a_very_secret_key_that_should_be_changed
    ```
    *`SECRET_KEY` sollte ein langer, zufälliger String sein.*

### 2. Datenbank starten

Die Anwendung ist so konfiguriert, dass sie eine MariaDB-Datenbank über Docker erwartet.

1.  **Erstellen Sie eine `docker-compose.yml`-Datei** im Stammverzeichnis des Projekts:
    ```yaml
    version: '3.8'
    services:
      mariadb:
        image: mariadb:10.5
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: root_password
          MYSQL_DATABASE: apt_erfolg_db
          MYSQL_USER: user
          MYSQL_PASSWORD: password
        ports:
          - "3306:3306"
        volumes:
          - mariadb_data:/var/lib/mysql

    volumes:
      mariadb_data:
    ```

2.  **Starten Sie den Datenbank-Container:**
    ```bash
    docker-compose up -d
    ```

### 3. Frontend einrichten

1.  **Navigieren Sie in das Frontend-Verzeichnis:**
    ```bash
    cd frontend
    ```

2.  **Installieren Sie die npm-Abhängigkeiten:**
    ```bash
    npm install
    ```

---

## Anwendung starten

1.  **Starten Sie den Backend-Server:**
    Stellen Sie sicher, dass Sie sich im `backend`-Verzeichnis befinden und Ihre virtuelle Umgebung aktiviert ist.
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    Die API ist jetzt unter `http://127.0.0.1:8000` verfügbar.

2.  **Starten Sie den Frontend-Server:**
    Öffnen Sie ein neues Terminal, navigieren Sie in das `frontend`-Verzeichnis und starten Sie den Angular-Entwicklungsserver.
    ```bash
    npm start
    ```
    Die Anwendung ist jetzt unter `http://localhost:4200` verfügbar.

    **Hinweis:** Derzeit gibt es ein hartnäckiges Build-Problem, das den Start des Frontend-Servers in der Testumgebung verhindert. Diese Anleitung beschreibt den beabsichtigten Startprozess.
