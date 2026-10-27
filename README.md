# FarmDirect Marketplace

A student project demonstrating a direct farm-to-consumer marketplace with a frontend and a Python Flask + SQLite backend.

## Features
- Responsive marketplace homepage
- Product catalogue stored in SQLite
- Search and category filters
- Shopping cart with quantity controls
- Customer delivery form
- Backend order validation and order storage
- Demo order list at `/admin/orders`
- Project credit: Created by Om Gaikwad

## Requirements
- Python 3.9 or newer
- pip

## Run on Windows
1. Extract the ZIP file.
2. Open Command Prompt inside the `farmdirect_marketplace` folder.
3. (Recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the server:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.
7. Demo orders can be viewed at `http://127.0.0.1:5000/admin/orders`.

## Run on macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## Important project limitations
- This is a local classroom demonstration, not a production e-commerce service.
- Orders are stored in a local SQLite database (`farmdirect.db`), created automatically on first run.
- No real payment, shipping, SMS, or email integration is included.
- `/admin/orders` is not password-protected; add authentication before hosting publicly.
- Change `app.secret_key` and disable debug mode before deployment.
