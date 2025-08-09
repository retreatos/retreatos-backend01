# RetreatOS Backend (Gallery + OAuth)

Flask API עם:
- Google OAuth
- העלאת תמונות ל-Cloudinary
- טבלאות משתמשים וגלריה (SQLAlchemy)
- CORS עם תמיכה ב-Credentials

## Env
- FLASK_SECRET_KEY=your-random-secret
- DATABASE_URL=sqlite:///local.db  (או Postgres של Render)
- FRONTEND_ORIGIN=https://your-frontend.onrender.com
- GOOGLE_CLIENT_ID=...
- GOOGLE_CLIENT_SECRET=...
- CLOUDINARY_CLOUD_NAME=...
- CLOUDINARY_API_KEY=...
- CLOUDINARY_API_SECRET=...
- POST_LOGIN_REDIRECT=https://your-frontend.onrender.com

## Start (local)
pip install -r requirements.txt
python app.py

## Render
Start Command: gunicorn app:app
