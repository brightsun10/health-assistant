---

# 🧠 AI Health Assistant – Powered by Gemini & Django

A smart, conversational health tracking assistant built with Django and powered by Gemini 1.5 Flash (Google Generative AI). The assistant can log meals, symptoms, and exercises conversationally and store them in a structured format for user-friendly tracking.

--- 

## 🔍 Project Overview

This project demonstrates how to:

Use LLM agents (Gemini) with tool/function calling

Store conversational health logs (meals, symptoms, exercises) in a database

Maintain chat context using memory

Build a modular, extensible AI agent in Django

Use environment variables for secure config

---

## 🚀 Features

🧠 Conversational Health Logging – Talk to your assistant like "I had dosa for breakfast" or "I felt dizzy at noon" and it'll log it automatically.

⚙️ Tool-Calling LLM Integration – Gemini model calls the internal log_health_data function using structured schema.

👤 User-Aware Logs – All data is tied to the currently logged-in user.

🗃️ Django Admin Access – View logs using Django admin panel.

📄 Structured Logging – Save logs as Meal, Symptom, or Exercise.

✅ Robust Error Handling – Gracefully handles model failures or malformed inputs.

---

## 🏗️ Tech Stack

Backend :	Django 4.2

AI Agent :	Google Gemini (via google-generativeai)

DB :	PostgreSQL (or SQLite by default)

Auth :	Django built-in authentication

Config :	python-dotenv + dj-database-url

---

## 📦 Setup Instructions

#### 1. Clone the Repository

git clone https://github.com/brightsun10/health-assistant.git

cd health-assistant

#### 2. Create a Virtual Environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

#### 3. Install Dependencies

pip install -r requirements.txt

#### 4. Set Environment Variables
Create a .env file and add:

GEMINI_API_KEY=your_google_generative_ai_key

SECRET_KEY=your_django_secret_key

DEBUG=True

DATABASE_URL=sqlite:///db.sqlite3  # Or your PostgreSQL URL

#### 5. Apply Migrations

python manage.py migrate

#### 6. Create Superuser (Optional)

python manage.py createsuperuser

#### 7. Run the Server

python manage.py runserver

## ✨ Example Usage

User Input:

I ate ragi mudde with sambar for lunch.

Gemini Response:

OK. I've logged that meal for you.

## 🧠 Agent Logic (agent.py)

Uses GenerativeModel from google-generativeai

Defines tool: log_health_data(log_type, content)

Gemini can reasonably decide when to call a tool vs give a normal reply

Stores logs in the HealthLog model

## 🔐 License
MIT License. Free to use and modify.

## Author

Made with ❤️ by Nithin P (brightsun10)

