# 🚀 FastAPI JWT Authentication & CRUD Backend

A production-ready backend application built with **FastAPI** that implements **JWT-based authentication**, **protected routes**, and **CRUD APIs for a secondary entity**.  
Designed to integrate seamlessly with a modern frontend (React / Vite) and deploy easily to cloud platforms.

---

## 📌 Overview

This project provides a secure REST API with user authentication and authorization using **JSON Web Tokens (JWT)**.  
Authenticated users can access protected endpoints and perform CRUD operations on a secondary entity such as tasks, notes, or items.

The project follows clean backend architecture and real-world best practices.

---

## ✨ Features

- User registration and login
- JWT-based authentication
- Secure password hashing (bcrypt)
- Protected routes using FastAPI dependencies
- CRUD APIs for a secondary entity
- Centralized error handling
- Environment-based configuration
- Ready for frontend integration
- Cloud-deployable architecture

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Python 3.10+
- SQLAlchemy ORM
- PostgreSQL / SQLite
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)

### Dev & Deployment
- Uvicorn
- python-dotenv
- Git & GitHub
- Compatible with Render / Railway / Fly.io

---

## 🔐 Authentication Flow

1. User registers via `/auth/register`
2. User logs in via `/auth/login`
3. Backend returns a JWT access token
4. Token is sent with every protected request:
