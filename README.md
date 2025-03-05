# beauty_shop_ecomm_website
## Development Setup

1. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

. **Set Up the Database**:
   - Run the following commands to initialize the database:
     ```bash
     flask db upgrade
     ```

5. **Run the Application with either of the 2 commands**:
   ```bash
   flask run
   ```
   ```or use
   python3 main.py  # Better option as you can refresh to view your changes
   ```
   - The app will be available at `http://127.0.0.1:5000/`.

---
