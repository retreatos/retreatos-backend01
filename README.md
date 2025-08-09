# RetreatOS Backend (Render Fix)

## Files
- app.py — Flask app with SQLAlchemy + Google OAuth. Creates tables at import-time under app context.
- requirements.txt — includes gunicorn so Render's `gunicorn app:app` works.
- Procfile — optional. Render ignores it, but useful for reference.

## Deploy on Render
1. Create a **Web Service** from this repo/zip.
2. Environment → add:
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET
   - FLASK_SECRET_KEY (random string)
   - DATABASE_URL (optional; default uses sqlite file)
3. **Start Command** (choose ONE):
   - Recommended: `gunicorn app:app`
   - Or for debugging: `python app.py`

4. OAuth redirect URI to add in Google Console:
   `https://YOUR_SERVICE_NAME.onrender.com/authorize`

If you still get `gunicorn: command not found`, make sure you redeploy after pushing `requirements.txt` that contains `gunicorn`.
