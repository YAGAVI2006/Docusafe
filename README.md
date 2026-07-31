# DOCUSAFE

A secure cloud-based document management system.

## Setup Instructions

1. **Install Dependencies:**
   Ensure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup:**
   By default, the application is configured to use MySQL (`mysql+pymysql://root:@localhost/docusafe`).
   Please ensure you have a MySQL server running and a database named `docusafe` created.
   
   To initialize the tables, run:
   ```bash
   python init_db.py
   ```

3. **Environment Variables:**
   You can create a `.env` file in the root directory and specify:
   ```
   SECRET_KEY=your_secret_key
   FERNET_KEY=your_32_url_safe_base64_encryption_key
   DATABASE_URL=mysql+pymysql://username:password@localhost/docusafe
   ```

4. **Run Backend:**
   ```bash
   python -m backend.app
   ```
   The backend will run on `http://localhost:5000`.

5. **Run Frontend:**
   You can open `frontend/index.html` directly in your browser, or serve it using a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Then navigate to `http://localhost:8000` in your browser.
