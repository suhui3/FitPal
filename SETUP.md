# FitPal — Team setup guide

This guide is for team members cloning the project fork, running it locally, and testing together.

## Prerequisites

- **Node.js** 18+ (LTS recommended) and **npm**
- **MongoDB** — local install or a shared [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) connection string from your team lead
- **Cloudinary** account — for profile picture uploads ([cloudinary.com](https://cloudinary.com))
- **Spoonacular** API key — for meal search and nutrition ([spoonacular.com/food-api](https://spoonacular.com/food-api))

## 1. Clone the repository

Clone the **team fork** URL your lead shares (not your personal fork unless instructed):

```bash
git clone <YOUR_TEAM_FORK_URL>
cd FitPal
```

Create your own branch for work:

```bash
git checkout -b your-name/feature-description
```

## 2. Install dependencies

Install in **three** places (root install is required for reminder cron support):

```bash
# From project root
npm install

cd backend
npm install

cd ../frontend
npm install
```

## 3. Environment variables

**Do not commit `.env` files.** Your team lead will send real values privately (chat, password manager, etc.) — not via GitHub.

### Backend

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`. See `backend/.env.example` for all variables.

| Variable | Purpose |
|----------|---------|
| `MONGODB_CONNECTION_STRING` | MongoDB connection (local or Atlas) |
| `JWT_SECRET_KEY` | Signs login cookies; team must use the **same** value for shared testing |
| `SPOONACULAR_API_KEY` | Meal search and nutrition API |
| `CLOUDINARY_CLOUD_NAME` | Profile image upload |
| `CLOUDINARY_KEY` | Cloudinary API key |
| `CLOUDINARY_SECRET` | Cloudinary API secret |
| `NODE_ENV` | Optional; use `development` locally |

**Generate a JWT secret (solo dev or new team secret):**

```bash
openssl rand -base64 32
```

Paste into `.env` **without quotes**:

```env
JWT_SECRET_KEY=yourGeneratedValueHere
```

Characters like `+` and `=` are fine.

**Cloudinary credentials:** Dashboard → **API Keys** → copy Cloud name, API Key, and API Secret (not an “upload token” — this project uses server-side upload with API key + secret).

### Frontend

```bash
cd frontend
cp .env.example .env
```

Default local config:

```env
VITE_API_BASE_URL=http://localhost:7001
```

Restart the frontend after changing `.env`.

## 4. Run the application

Use **two terminals**.

**Terminal 1 — backend** (port `7001`):

```bash
cd backend
npm run dev
```

Expected output includes:

- `Connected to database`
- `Server is running on http://localhost:7001`

**Terminal 2 — frontend** (port `5173`):

```bash
cd frontend
npm run dev
```

Open the URL Vite prints (usually **http://localhost:5173**).

> **Note:** Use `npm run dev`, not `npm start`. The README may list `npm start`; this repo uses `dev` scripts.

## 5. Quick smoke test

1. Register a new account.
2. Sign in.
3. Complete profile — **select a profile image** if testing upload (Cloudinary must be configured).
4. Try meal search (requires valid Spoonacular key).
5. Create a reminder (Socket.IO notifications use `http://localhost:7001`).

## Team workflow summary

| Topic | Recommendation |
|-------|----------------|
| Git | Clone team fork → branch per member → PRs to shared branch/main |
| Secrets | Same MongoDB / Cloudinary / JWT / Spoonacular for shared dev — share **privately**, never in git |
| JWT | Everyone on shared testing must use the **same** `JWT_SECRET_KEY` |
| Database | Shared Atlas DB = shared users and data; coordinate so testers don’t overwrite each other’s work unexpectedly |
| Forking | Members clone the **lead’s fork**; only fork again if your course requires it |

## Ports and URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:7001 |
| API base path | `/api/...` (e.g. `/api/auth/login`) |

CORS is configured for `http://localhost:5173` only. Use `localhost` consistently (not `127.0.0.1` on one side and `localhost` on the other) to avoid cookie issues.

## Troubleshooting

### `Cannot find module 'node-cron'`

Run `npm install` in the **project root**, then restart the backend.

### `cloud_name is disabled` or Cloudinary 401

- Check `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_KEY`, and `CLOUDINARY_SECRET` in `backend/.env`.
- Restart the backend after editing `.env`.
- Upload a file when creating/updating profile (field name must be `imageFile`).

### `Cannot read properties of undefined (reading 'buffer')`

Profile upload was called without an image file. Select an image before submitting create/update profile.

### API calls fail / `undefined` in network tab

- Set `VITE_API_BASE_URL=http://localhost:7001` in `frontend/.env`.
- Restart the frontend dev server.

### Unauthorized after changing `JWT_SECRET_KEY`

Log out and log in again. Old cookies were signed with the previous secret.

### Meal search does nothing / API errors

Set a valid `SPOONACULAR_API_KEY`. Free tier has daily request limits shared across the team if you use one key.

### MongoDB connection errors

- Local: ensure MongoDB is running and the connection string is correct.
- Atlas: whitelist your IP in Network Access and verify username/password in the URI.

## Project structure

```text
FitPal/
├── backend/          # Express API, Socket.IO, MongoDB
│   ├── .env.example
│   └── src/
├── frontend/         # React + Vite
│   ├── .env.example
│   └── src/
├── package.json      # Root deps (includes node-cron for backend)
└── SETUP.md          # This file
```

## Security reminders

- Never push `.env` to GitHub (`.env` is gitignored in `backend/` and `frontend/`).
- Do not paste API keys in issues, PRs, or public channels.
- Rotate Cloudinary or Atlas credentials if they are ever exposed.

For feature overview and tech stack, see [README.md](./README.md).
