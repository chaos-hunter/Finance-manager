# Finance Manager

Finance Manager is a Django-based application for managing wallets and transactions.

## Running locally on Windows (Command Prompt)
Follow these steps to set up and run the project on Windows using Command Prompt.

1. **Install prerequisites**
   - Install [Python 3.11+](https://www.python.org/downloads/windows/) and ensure `python` is available in Command Prompt.
   - Install [Git](https://git-scm.com/download/win).

2. **Clone the repository**
   ```cmd
   git clone <repo-url>
   cd Finance-manager
   ```

3. **Create and activate a virtual environment**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. **Install Python dependencies**
   ```cmd
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Apply database migrations**
   ```cmd
   python manage.py migrate
   ```

6. **Create or reuse the SQLite database**
   - To start fresh, Django will create `db.sqlite3` on the first migration.
   - If the repository already includes `db.sqlite3`, you can reuse it or delete it before migrating to start clean.

7. **Run the development server**
   ```cmd
   python manage.py runserver
   ```
   Then open http://127.0.0.1:8000/ in your browser.
   - The project already includes `127.0.0.1` and `localhost` in `ALLOWED_HOSTS` so you should not see `DisallowedHost` errors when using the default address.

8. **Run tests (optional)**
   ```cmd
   python manage.py test
   ```

### Notes
- The React UI is bundled in `static/js/react-ui.js` and served directly via Django's static files; no Node.js build is required.
- On first run, Windows may prompt to allow Python through the firewall for local connections.

