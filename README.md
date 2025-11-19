# FitPal – Health & Fitness Tracking System
FitPal is a feature-rich, user-centric health and fitness tracking application built using the MERN stack. The system helps users monitor daily workouts, track calorie intake, visualize progress, and manage personalized meal plans through intelligent recommendations powered by the Spoonacular API. With a clean UI and responsive design, FitPal empowers users to stay consistent in their fitness journey through structured routines, nutrition planning, and timely reminders.

# Features

### 🔐 General & Authentication

- User registration, login, and logout

- JWT-based authentication

- Secure password hashing

- Account deactivation and profile updates

### 💪 Fitness Tracker
- Log daily workouts, steps, and cardio activities

- Track calories burned

- View daily and weekly fitness summaries

### 📊 Progress & Analytics

- Dynamic progress charts

- Calorie intake vs. calories burned comparisons

### 🍽️ Nutrition Planner

- Meal planning with intelligent recommendations

- Spoonacular API integration

- Detailed nutritional breakdowns

- Add to planner & favourites

### ⏰ Notifications & Reminders
- Set personalized reminders for workouts and meals

- View, edit, and manage reminders in-app

# Tech Stack

**Frontend**: React, Bootstrap <br />
**Backend**: Node.js, Express <br />
**Database**: MongoDB <br />
**Auth & Security**: JWT, bcrypt <br />
**API**: Spoonacular <br />

# Setup

1. Clone the repo

`git clone https://github.com/Calvern/FitPal.git`


2. Install dependencies

- Backend: `cd backend && npm install`

- Frontend: `cd frontend && npm install`

3. Configure `.env`

- Backend: `MONGO_URI`, `JWT_SECRET`, `SPOONACULAR_API_KEY`


4. Run the app

- Backend: `npm start` (in `backend/`)

- Frontend: `npm start` (in `frontend/`)
