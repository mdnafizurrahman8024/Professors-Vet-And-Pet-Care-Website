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

### The short command (Windows)

```
python run_server.py
```

That is all. It automatically:

1. installs any missing dependencies from `requirements.txt`,
2. **picks a free port** — if `8000` is already used by another app it moves to `8001`, `8002`, … (so the server can never crash with *"That port is already in use"*),
3. creates the `static/` and `media/` folders if they were deleted,
4. runs `manage.py check` and stops with a clear message if something is misconfigured,
5. applies pending migrations, then starts the server.

The terminal prints the exact URL to open, e.g. `http://127.0.0.1:8001/`.

Useful variants:

```
python run_server.py 8010        # force a specific port
python run_server.py --noreload  # disable auto-reload
start.bat                        # double-click launcher (same thing)
.\start.ps1                      # PowerShell version
```

> After adding new features (new app → `python manage.py makemigrations` +
> `python run_server.py`), the launcher keeps working: it re-runs the Django
> system check and applies any new migrations automatically.

### Manual steps (optional)

```bash
python manage.py migrate        # apply migrations
python manage.py seed_data      # seed demo products / schedules / clinic info
python manage.py runserver 8000 # plain Django server
```
Visit `http://127.0.0.1:8000/` in your browser.
