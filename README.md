# Professor's Vet & Pet Care Web Application

A full-stack, production-ready web application and pet e-commerce platform built for **Professor's Vet & Pet Care**, located at 138 Debishing Para, Madrashar More, Rajshahi, Bangladesh.

Supervised by **Dr. Abdulla Al Mamun Bhuyan** — Associate Professor, Department of Veterinary and Animal Sciences, University of Rajshahi.

---

## 🚀 Production & Cloud Hosting Deployment Guide

This project is completely configured for seamless production deployment on platforms such as **Render**, **Railway**, or **PythonAnywhere**.

### Option A: Deploy on Render (Recommended)

1. Push this codebase to your GitHub or GitLab repository.
2. In the [Render Dashboard](https://dashboard.render.com/), click **New** ➔ **Web Service**.
3. Connect your repository. Render will automatically detect [`render.yaml`](file:///d:/A.Technical%20Skill/Professor's%20Vet%20&%20Pet%20Clinic%20Website/render.yaml) and [`Procfile`](file:///d:/A.Technical%20Skill/Professor's%20Vet%20&%20Pet%20Clinic%20Website/Procfile).
4. Configure the build & start commands:
   * **Build Command:** `./build.sh` (or `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py seed_data`)
   * **Start Command:** `gunicorn vetcare.wsgi:application`
5. Under **Environment Variables**, set:
   * `DEBUG` = `False`
   * `SECRET_KEY` = *(click Generate or supply a secure string)*
   * `ALLOWED_HOSTS` = `*`
6. Click **Create Web Service**. Your live clinic site will be deployed with HTTPS in minutes.

---

### Option B: Deploy on Railway

1. In [Railway.app](https://railway.app/), click **New Project** ➔ **Deploy from GitHub repo**.
2. Select your repository. Railway automatically reads the [`Procfile`](file:///d:/A.Technical%20Skill/Professor's%20Vet%20&%20Pet%20Clinic%20Website/Procfile) and [`requirements.txt`](file:///d:/A.Technical%20Skill/Professor's%20Vet%20&%20Pet%20Clinic%20Website/requirements.txt).
3. In your project settings, add the environment variables:
   * `DEBUG` = `False`
   * `ALLOWED_HOSTS` = `*`
   * `SECRET_KEY` = *(a random string)*
4. If you add a PostgreSQL plugin on Railway, Railway will automatically provide a `DATABASE_URL` variable which the app will connect to automatically!

---

### Option C: Deploy on PythonAnywhere

1. Upload or clone your repository to your PythonAnywhere directory:
   ```bash
   git clone <your-repo-url>
   ```
2. Create and activate a virtualenv:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```
3. Run migrations and collect static files:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py seed_data
   ```
4. In the **Web** tab:
   * Point your **Virtualenv** to `myenv`.
   * In the **WSGI configuration file**, point to `vetcare.wsgi:application`.
   * Set up Static and Media paths:
     * URL: `/static/` ➔ Directory: `/home/<username>/.../staticfiles`
     * URL: `/media/` ➔ Directory: `/home/<username>/.../media`
5. Reload your web app.

---

## 🔑 Default Superuser & Demo Credentials

* **Admin URL:** `/admin/`
* **Email / Login:** `bhuyan@ru.ac.bd`
* **Phone:** `+8801316254500`
* **Username:** `admin`
* **Password:** `admin`

---

## 🛠️ Local Development

```bash
# 1. Apply database migrations
python manage.py migrate

# 2. Seed initial sample products, schedules, and clinic info
python manage.py seed_data

# 3. Start local development server
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.
