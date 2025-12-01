# SupportPilot

SupportPilot — Smart Customer Support Automation System

This repository contains a full-stack customer support automation system built with:
- Backend: Python Flask
- Frontend: React
- Database: Supabase (Auth, Postgres, Storage)
- AI/ML: Basic sentiment analysis, priority prediction, keyword extraction

This project is scaffolded for local development and demonstration.

## Quickstart (Development)

Prerequisites:
- Python 3.10+
- Node 18+ and npm
- Supabase account (for production features)

Backend setup

1. Create and activate a Python virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

2. Set environment variables (optionally in `.env`):

   - `SUPABASE_URL` - your Supabase URL
   - `SUPABASE_KEY` - your Supabase service role key
   - `JWT_SECRET_KEY` - secret for JWT tokens

3. Run the Flask app:

   ```bash
   cd backend
   python app.py
   ```

4. (Optional) Train sample ML models:

   ```bash
   cd backend/ml
   python train_models.py
   ```

Frontend setup

1. Install dependencies and start dev server:

   ```bash
   cd frontend
   npm install
   npm start
   ```

2. Open `http://localhost:3000`.

Testing

- Backend tests (pytest):
  ```bash
  cd backend
  pytest
  ```

- Frontend tests (React Testing Library):
  ```bash
  cd frontend
  npm test
  ```

Supabase

This project expects several tables in Supabase:
- `users` (user profiles)
- `tickets` (tickets)
- `comments` (ticket comments)
- `attachments` (file metadata)
- `agent_performance` (agent metrics)
- `audit_logs` (audit entries)
- `notifications` (in-app notifications)

Refer to `docs/ER_diagram.txt` for a simple ER layout.

API

The backend exposes REST endpoints under `/api`:
- `POST /api/auth/register` — register
- `POST /api/auth/login` — login
- `POST /api/tickets` — create ticket
- `GET /api/tickets/<id>` — get ticket
- `PUT /api/tickets/status/<id>` — update status
- `POST /api/tickets/assign/<id>` — assign ticket
- `GET /api/analytics/dashboard` — admin dashboard stats

See `docs/API_DOCS.md` for more details.

Security and Production Notes

- Replace development secrets before production.
- Use Supabase Auth for secure user/password management.
- Configure CORS appropriately.

License

MIT
