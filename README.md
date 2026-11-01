<!-- ───────────────────────── HERO BANNER ───────────────────────── -->
<div align="center">

<img src="Logo.png" alt="Professor's Vet & Pet Care logo" width="120" />

# 🐾 Professor's Vet & Pet Care

### A production-ready veterinary clinic platform and pet e-commerce store — appointments, surgery gallery, prescriptions and inventory in one Django application

**138 Debishing Para, Madrashar More, Rajshahi, Bangladesh**

*Supervised by **Dr. Abdulla Al Mamun Bhuyan** — Associate Professor, Department of Veterinary and Animal Sciences, University of Rajshahi*

<br/>

[![Primary Language](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Django_5+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/SQLite_%2F_PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Render_%7C_Railway_%7C_PythonAnywhere-46E3B7?style=for-the-badge&logo=render&logoColor=white)](#-production--cloud-hosting-deployment-guide)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=for-the-badge&logo=statuspage&logoColor=white)](#)
[![Author](https://img.shields.io/badge/Author-Md._Nafizur_Rahman-0F4C81?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mdnafizurrahman8024)

<br/>

🏥 **Clinic Management** · 🛍️ **Pet E-Commerce** · 📅 **Appointment Booking** · 🩺 **Surgery Case Gallery** · 🌐 **Bangla + English UI**

</div>

---

## 📖 Overview

**Professor's Vet & Pet Care** is a full-stack, production-ready **Django** web application serving a real
veterinary clinic in **Rajshahi, Bangladesh**. It unifies the two halves of a modern veterinary practice:

- **Clinical operations** — doctor scheduling, appointment booking, patient (pet) records, and
  digital prescription capture with an auditable medical history.
- **Retail operations** — a bilingual pet-supply storefront with a session-based cart, live stock
  checks, prescription-gated medicines, and bKash / Nagad / card / cash-on-delivery checkout.

Everything is driven from a **customised Django admin panel** titled *"Clinic & E-Commerce
Management"*, where staff manage products, appointments, surgery cases, notice-board offers and
clinic contact information without touching code.

> 🎯 **Design goal** — a clinic owner should be able to deploy this in minutes and run their entire
> front desk from one dashboard, on a free-tier cloud host, with HTTPS and zero server maintenance.

---

## ✨ Key Features

### 🏥 Clinic & Appointments
- **📅 Weekly doctor schedule** — per-day availability (Sat–Fri), configurable start/end hours,
  **20-minute slot duration** and max patients per slot, editable from the admin.
- **🩺 Service-driven booking** — 8 clinical categories including *General Health Checkup*,
  *Vaccination & Deworming*, *Surgery Consultation*, *Orthopedic & Fracture Care*,
  *Dental & Oral Hygiene*, *Emergency & Trauma Care*, *Skin & Dermatology* and *Diagnostic Follow-up*.
- **🔖 Human-readable booking IDs** — auto-generated as `APT-YYMM-XXXXX` for confident phone follow-up.
- **📝 Clinical record capture** — doctor advice, prescribed medicines, consultation fee (default
  BDT 500) and payment status stored per appointment.

### 🐕 Pet Patient Records
- **Owner-scoped pet profiles** — species (Dog, Cat, Bird, Rabbit, Fish, Other), breed, gender,
  age in years + months, weight, **microchip ID**, photo and full medical history.
- **👤 Dual-identifier authentication** — log in with **either email or phone** via a custom
  `EmailOrPhoneBackend`; usernames are auto-derived when registering.
- **🔁 Password reset** flow included (console email backend for local testing).

### 🛍️ Pet E-Commerce Storefront
- **🗂️ Five curated categories** — Pet Food, Veterinary Medicine, Toys & Play, Accessories &
  Collars, and Grooming & Hygiene, each with a Lucide icon.
- **🐾 Target-pet filtering** — surfaces products per species (Dog / Cat / Bird / Rabbit / All).
- **💸 Discount engine** — automatic `current_price`, `discount_percentage` and strike-through pricing.
- **📦 Live inventory intelligence** — `in_stock` / `low_stock` (≤ 5 units) / `out_of_stock`
  states, surfaced to the cart via an AJAX stock endpoint.
- **🛒 Session cart with hard stock ceilings** — quantities are clamped server-side so an order can
  never exceed available units.
- **💊 Prescription-gated medicines** — mark any product `is_prescription_required`; checkout then
  demands a prescription upload attached to the order.
- **💳 Local payment rails** — Cash on Delivery, **bKash**, **Nagad** and Debit/Credit Card, each
  with a transaction-ID field and UNPAID / PAID / REFUNDED tracking.
- **🚚 Order lifecycle** — PENDING → CONFIRMED → PROCESSING → SHIPPED → DELIVERED (or CANCELLED),
  with a BDT 60 Rajshahi delivery fee and auto-generated `ORD-XXXXXXXX` numbers.

### 🩺 Surgery Case Gallery
- **📸 Clinical case studies** — categorised surgeries with diagnosis summary, procedure details,
  recovery outcome and chief surgeon.
- **🖼️ Before / after imagery** plus an optional **video walkthrough** URL.
- **👁️ View counters and featured flags** to promote standout cases on the homepage.

### 🎯 Marketing & Clinic Info
- **📢 Notice & offer engine** — marquee ticker + hero banners for *Special Offers*, *Clinic
  Notices*, *Free Health Camps* and *Emergency Alerts*, with discount codes, date windows and
  priority ordering.
- **🗺️ Centralised clinic profile** — doctor degrees, designation, chamber and physical address,
  satellite map embed, operating hours and emergency contact, all editable from admin and injected
  globally through a context processor.
- **🌐 Fully bilingual** — UI labels, product categories and service names ship in **English and
  বাংলা (Bangla)** side by side.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.12 |
| **Web Framework** | Django 5.x (custom `AUTH_USER_MODEL`, context processors) |
| **Database** | SQLite by default · PostgreSQL via `DATABASE_URL` (`dj-database-url`) |
| **Static Files** | WhiteNoise (`CompressedStaticFilesStorage`) |
| **Media / Images** | Pillow |
| **Config** | `python-dotenv` + environment variables |
| **WSGI Server** | Gunicorn (Linux) · Waitress (Windows fallback) |
| **Templating** | Django templates + Tailwind-style utility classes |
| **Frontend JS** | Vanilla ES6 — AJAX cart, live stock, toast notifications |
| **Deployment** | Render (`render.yaml`), Railway (`Procfile`), PythonAnywhere |

---

## 🏗️ Architecture & Directory Tree

```
Professors-Vet-And-Pet-Care-Website/
├── 🧠 vetcare/                    # Project configuration package
│   ├── settings.py                # Env-driven config · WhiteNoise · security hardening
│   ├── urls.py                    # Root URLconf + branded admin header + media serving
│   ├── wsgi.py / asgi.py          # Server entry points
│
├── 👤 accounts/                   # Authentication & pet patients
│   ├── models.py                  # CustomUser · Pet · CustomUserManager
│   ├── backends.py                # EmailOrPhoneBackend (dual-identifier login)
│   ├── forms.py · views.py        # Register · login · dashboard · add/delete pet
│
├── 📅 appointments/               # Scheduling engine
│   ├── models.py                  # DoctorSchedule · Appointment (8 service types)
│   └── views.py                   # Booking flow + success confirmation
│
├── 🛍️ shop/                       # E-commerce core
│   ├── models.py                  # Category · Product · Order · OrderItem
│   ├── cart.py                    # Session cart with stock clamping
│   ├── context_processors.py      # Cart badge available on every page
│   └── views.py                   # Shop · product · AJAX cart · checkout · stock API
│
├── 🩺 gallery/                    # Surgical case library
│   └── models.py                  # SurgeryCategory · SurgeryCase (before/after media)
│
├── 🏥 core/                       # Clinic identity & marketing
│   ├── models.py                  # NoticeOffer · ClinicInfo
│   ├── context_processors.py      # Global clinic context for all templates
│   └── management/commands/seed_data.py   # Idempotent demo seeder
│
├── 🎨 templates/                  # base.html + per-app template folders
│   └── core/ shop/ accounts/ appointments/ gallery/
├── 🖼️ static/js/cart.js           # AJAX cart, toasts, live inventory
├── 📁 media/                      # User uploads (avatars, products, surgeries, Rxs)
│
├── 🚀 run_server.py               # Smart local launcher (auto-port, auto-migrate)
├── 🪟 start.bat · start.ps1       # One-click launchers
├── ⚙️ build.sh                    # Production build script
├── 📋 Procfile                    # Gunicorn process definition
├── ☁️ render.yaml                 # Render blueprint (Python 3.12 + generated SECRET_KEY)
├── 🔑 .env.example                # Environment variable template
├── 📦 requirements.txt
└── 🖼️ Logo.png · Doctor.png
```

### 🔄 Core Request Flow

```
Browser ──▶ Django URLconf (vetcare/urls.py)
              ├── /            → core.views.home      (featured products + surgery cases)
              ├── /accounts/   → register · login · dashboard · pets · password reset
              ├── /appointments/ → schedule-aware booking → APT-YYMM-XXXXX
              ├── /shop/       → catalog · AJAX cart · checkout · order confirmation
              ├── /gallery/    → surgery cases with before/after media
              └── /admin/      → Django admin (clinic & commerce back office)
                                      │
                    ┌─────────────────┴─────────────────┐
              SQLite / PostgreSQL                 WhiteNoise (compressed static)
```

---

## 🚀 Local Development

### ✅ Prerequisites

- **Python 3.10+** (3.12 recommended — matches `render.yaml`)
- `pip` and, optionally, a virtual environment

### ⚡ The short command (Windows)

```bash
python run_server.py
```

That is all. It automatically:

1. **installs any missing dependencies** from `requirements.txt`,
2. **picks a free port** — if `8000` is already taken by another app it moves to `8001`, `8002`, …
   (so the server can never crash with *"That port is already in use"*),
3. **creates the `static/` and `media/` folders** if they were deleted,
4. runs `manage.py check` and **stops with a clear message** if something is misconfigured,
5. **applies pending migrations**, then starts the server.

The terminal prints the exact URL to open, e.g. `http://127.0.0.1:8001/`.

**Useful variants**

```bash
python run_server.py 8010        # force a specific port
python run_server.py --noreload  # disable auto-reload
start.bat                        # double-click launcher (same thing)
.\start.ps1                      # PowerShell version
```

> 💡 After adding new features (new app → `python manage.py makemigrations` +
> `python run_server.py`), the launcher keeps working: it re-runs the Django system check and
> applies any new migrations automatically.

### 🧰 Manual steps (any OS)

```bash
# 1. Set up a virtual environment
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment (optional for local dev)
cp .env.example .env

# 4. Prepare the database
python manage.py migrate          # apply migrations
python manage.py seed_data        # seed demo products / schedules / clinic info

# 5. Run
python manage.py runserver 8000   # plain Django server
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## 🔑 Default Superuser & Demo Credentials

| Field | Value |
| :--- | :--- |
| **Admin URL** | `/admin/` |
| **Username** | `admin` |
| **Password** | `admin` |
| **Email / Login** | `bhuyan@ru.ac.bd` |
| **Phone** | `+8801316254500` |

> ⚠️ **Change the default password before any public deployment.** Set a strong, unique
> `SECRET_KEY` and rotate these credentials in production.

---

## ⚙️ Environment Variables

Copy [`.env.example`](./.env.example) to `.env` and adjust:

| Variable | Purpose | Example |
| :--- | :--- | :--- |
| `SECRET_KEY` | Django cryptographic signing key | *(64-char random string)* |
| `DEBUG` | Debug mode — **must be `False` in production** | `False` |
| `ALLOWED_HOSTS` | Comma-separated hosts, or `*` | `myapp.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | Trusted HTTPS origins for CSRF | `https://myapp.onrender.com` |
| `DATABASE_URL` | Database connection string (blank ⇒ SQLite) | `sqlite:///db.sqlite3` |

> 🔒 When `DEBUG=False`, the app automatically enables `SESSION_COOKIE_SECURE`,
> `CSRF_COOKIE_SECURE`, `SECURE_CONTENT_TYPE_NOSNIFF` and `X_FRAME_OPTIONS='DENY'`.
> Locally, `run_server.py` forces `DEBUG=True` so HTTP logins and form posts work on `127.0.0.1`.

---

## ☁️ Production & Cloud Hosting Deployment Guide

This project is completely configured for seamless production deployment on platforms such as
**Render**, **Railway**, or **PythonAnywhere**.

### Option A: Deploy on Render *(recommended)*

1. Push this codebase to your GitHub or GitLab repository.
2. In the [Render Dashboard](https://dashboard.render.com/), click **New** ➔ **Web Service**.
3. Connect your repository. Render will automatically detect [`render.yaml`](./render.yaml) and
   [`Procfile`](./Procfile).
4. Configure the build & start commands:
   - **Build Command:** `./build.sh`
     *(or `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py seed_data`)*
   - **Start Command:** `gunicorn vetcare.wsgi:application`
5. Under **Environment Variables**, set:
   - `DEBUG` = `False`
   - `SECRET_KEY` = *(click Generate or supply a secure string)*
   - `ALLOWED_HOSTS` = `*`
6. Click **Create Web Service**. Your live clinic site will be deployed with HTTPS in minutes.

### Option B: Deploy on Railway

1. In [Railway.app](https://railway.app/), click **New Project** ➔ **Deploy from GitHub repo**.
2. Select your repository. Railway automatically reads the [`Procfile`](./Procfile) and
   [`requirements.txt`](./requirements.txt).
3. In your project settings, add the environment variables:
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*`
   - `SECRET_KEY` = *(a random string)*
4. If you add a **PostgreSQL plugin** on Railway, Railway will automatically provide a
   `DATABASE_URL` variable which the app will connect to automatically! 🎉

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
   - Point your **Virtualenv** to `myenv`.
   - In the **WSGI configuration file**, point to `vetcare.wsgi:application`.
   - Set up Static and Media paths:
     - URL: `/static/` ➔ Directory: `/home/<username>/.../staticfiles`
     - URL: `/media/` ➔ Directory: `/home/<username>/.../media`
5. **Reload** your web app.

---

## 🗺️ Future Roadmap

| Status | Milestone |
| :--- | :--- |
| ✅ Done | Django 5 clinic + e-commerce monolith with custom user model |
| ✅ Done | Email-or-phone authentication with pet profiles |
| ✅ Done | Schedule-driven appointment booking with `APT-YYMM` references |
| ✅ Done | Session cart, live stock API and prescription-gated checkout |
| ✅ Done | Surgery case gallery with before/after media |
| 🔄 In progress | Real bKash / Nagad payment gateway integration (replacing TrxID entry) |
| 🔄 In progress | SMS/WhatsApp appointment confirmations and reminders |
| 🧭 Planned | Printable PDF prescriptions and invoices |
| 🧭 Planned | SMS-based owner notifications for vaccination due dates |
| 🧭 Planned | Multi-doctor support with per-vet calendars |
| 🧭 Planned | Inventory expiry alerts driven by `Product.expiry_date` |

---

## 🤝 Contributing

```bash
git checkout -b feature/your-feature-name
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
```

Then open a **Pull Request**. Please run the Django checks and the test suite before submitting:

```bash
python manage.py check
python manage.py test
```

Licensed under the **MIT License** — see [LICENSE](./LICENSE).

---

<br/>

<!-- ───────────────────────── AUTHOR ───────────────────────── -->
<div align="center">

## 👨‍🔬 Author & Connect

### Md. Nafizur Rahman

**Undergraduate Student** · Faculty of Veterinary and Animal Sciences<br/>
University of Rajshahi, Rajshahi-6205, Bangladesh

<br/>

[![Email](https://img.shields.io/badge/Email-s2210968138%40ru.ac.bd-0F4C81?style=for-the-badge&logo=gmail&logoColor=white)](mailto:s2210968138@ru.ac.bd)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-%2B8801949288024-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/8801949288024)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-md--nafizur--rahman--ru-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](http://www.linkedin.com/in/md-nafizur-rahman-ru)
[![GitHub](https://img.shields.io/badge/GitHub-mdnafizurrahman8024-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mdnafizurrahman8024)

<br/>

[![CV](https://img.shields.io/badge/📄_Curriculum_Vitae-View-1B4D8C?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/file/d/106-eTtiqsvXZ9PIY_shcyWJX9kR66uq9/view?usp=drive_link)
[![Portfolio](https://img.shields.io/badge/🌐_Portfolio-Explore-5AA9E6?style=for-the-badge&logo=googlechrome&logoColor=white)](https://sites.google.com/view/md-nafizur-rahman/home)
[![Facebook](https://img.shields.io/badge/Facebook-mdnafizurrahman8024-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/mdnafizurrahman8024/)

<br/>

**Research Identifiers**

[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--3918--187X-A6CE39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0009-0008-3918-187X)
[![Google Scholar](https://img.shields.io/badge/Google_Scholar-bImpEzMAAAAJ-4285F4?style=for-the-badge&logo=googlescholar&logoColor=white)](https://scholar.google.com/citations?user=bImpEzMAAAAJ&hl=en)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Md--Rahman--1097-00CCBB?style=for-the-badge&logo=researchgate&logoColor=white)](https://www.researchgate.net/profile/Md-Rahman-1097)
[![OSF](https://img.shields.io/badge/OSF-10.17605%2FOSF.IO%2F9AQS3-2F3136?style=for-the-badge&logo=osf&logoColor=white)](https://doi.org/10.17605/OSF.IO/9AQS3)

<br/>

**Contact**

📧 [s2210968138@ru.ac.bd](mailto:s2210968138@ru.ac.bd) &nbsp;·&nbsp;
📞 [+8801949288024](https://wa.me/8801949288024) &nbsp;·&nbsp;
📍 Rajshahi-6205, Bangladesh

</div>

<br/>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:1C4C34,50:2E8B57,100:5AA9E6&height=110&section=footer&animation=fadeIn" alt="" />

<div align="center">

<sub>⭐ <i>Expert veterinary medicine, surgery and premium pet care — code-built for Rajshahi.</i></sub>

</div>
