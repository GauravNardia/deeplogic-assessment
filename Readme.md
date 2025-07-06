# 🐛 DeepLogic Assessment - Issue Tracker

A full-stack **issue tracking system** built with **FastAPI + SvelteKit**, designed for real-world software teams with role-based access and modern tooling.

---

## 🔧 Tech Stack

| Layer      | Tech                    |
|------------|-------------------------|
| Frontend   | SvelteKit + TailwindCSS |
| Backend    | FastAPI + SQLAlchemy    |
| Database   | PostgreSQL (via Docker) |
| Auth       | JWT (Secure Login)      |
| Charts     | Chart.js                |
| API Docs   | Swagger (OpenAPI)       |

---

## 🚀 Features

- ✅ **JWT Authentication** (Register, Login, Secure API access)
- ✅ **Role-based Issue Tracker**  
  - **Reporter**: Submit and view own issues  
  - **Maintainer**: Manage assigned issues  
  - **Admin**: Full control (create, edit, assign, chart)
- ✅ **Dark Mode UI**
- ✅ **Markdown Support** for issue descriptions
- ✅ **Real-Time Chart** (Issues by severity)
- ✅ **Auto-generated Swagger Docs** (`/api/docs`)
- ⚠️ **Background Aggregation Task** – *Planned but skipped for simplicity*

---

## 🐳 Run with Docker

```bash
docker-compose up --build