# 🧪 MoodBrew — The Emotional Alchemy Lab
> **Unit 3 App Development Review &bull; 5 Marks Evaluation**  
> Built with Django 6.1, SQLite, WhiteNoise, Claymorphism + Maximalism Design, and configured for Serverless Deployment on Vercel.

---

## 🔮 Concept: Not Your Average Generic Web App

Instead of another cookie-cutter todo app, blog, or standard dashboard, **MoodBrew** is an **Emotional Alchemy Lab** — a personal reflective mood journal disguised as an artisanal potion-brewing lab.

- **Emotion Ingredients**: Mix feelings (Joy 😄, Peace 🕊️, Anxiety 😰, Hope 🌱, Exhaustion 😴, Nostalgia 📷, Anger 🔥) into bespoke emotional recipes.
- **The Cauldron**: Name your brew (e.g., *"Sunday Morning Sunbeam"*, *"3am Overthinking Elixir"*, *"First Day Jitters Tonic"*), set the vibe meter from 1 (💀 Rough) to 10 (✨ Magical), and write reflections.
- **Design Philosophy**: **Claymorphism + Maximalism** — warm peachy background gradients, puffy 3D clay-pressed cards, soft multi-layer inset shadows, bold saturated emotion chips, and playful tactile typography. Genuinely human, thoughtful, and expressive.

---

## 🎯 Syllabus &amp; Rubric Alignment (Total: 5 Marks)

| Evaluation Component | Marks | Implementation in MoodBrew | Code Reference |
|---|:---:|---|---|
| **1. Installation of Django** | **1 Mark** | Django 6.1.1 configured with modular architecture (`config/` and `potions/`), `requirements.txt`, WhiteNoise static pipeline, environment-aware `settings.py`, and SQLite `/tmp` serverless fallback. | [`config/settings.py`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/config/settings.py), [`requirements.txt`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/requirements.txt) |
| **2. Template Usage** | **1 Mark** | `base.html` master layout with template inheritance (`{% block %}`), reusable components (`footer.html`), authentication-aware navigation, CSRF tokens, Django messages framework, and custom template filters (`brew_tags.py`: `vibe_stars`, `vibe_emoji`, `chip_html`, `percentage`). | [`templates/base.html`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/templates/base.html), [`potions/templatetags/brew_tags.py`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/potions/templatetags/brew_tags.py) |
| **3. Model and Views** | **2 Marks** | Relational data models (`EmotionIngredient` and `Potion` with `ForeignKey` to `User`, `ManyToManyField`, validation, and computed properties). Authentication views (`LoginView`, `LogoutView`, `RegisterView`) and 6 Core Views (`DashboardView`, `PotionListView`, `PotionDetailView`, `PotionCreateView`, `PotionUpdateView`, `PotionDeleteView`, `toggle_favorite`) with dynamic Q-search and aggregation. | [`potions/models.py`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/potions/models.py), [`potions/views.py`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/potions/views.py), [`potions/forms.py`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/potions/forms.py) |
| **4. Output** | **1 Mark** | Tactile claymorphic UI with floating emojis, interactive vibe slider, ingredient checkbox pills, vibe weather distribution bars, bookmark stars, pre-seeded realistic human journal entries, and responsive layouts. | [`templates/potions/dashboard.html`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/templates/potions/dashboard.html), [`static/css/style.css`](file:///C:/Users/kotir/.gemini/antigravity/scratch/moodbrew/static/css/style.css) |

---

## 🔑 Demo Credentials (For Evaluation &amp; Review)

| Role | Username | Password |
|---|---|---|
| **Lead Alchemist (Pre-seeded)** | `alchemist` | `brew1234` |
| **New Users** | Sign up via `/register/` anytime! | Custom |

---

## ⚡ Quick Start (Local Setup)

### 1. Prerequisites &amp; Installation
Ensure Python (3.10+) is installed. Navigate to the project directory:
```bash
cd C:\Users\kotir\.gemini\antigravity\scratch\moodbrew
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Apply Migrations &amp; Seed Initial Potions
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### 3. Run Development Server
```bash
python manage.py runserver
```
Open **`http://127.0.0.1:8000/`** in your browser.

---

## 🧪 Automated Testing

MoodBrew comes with 20 unit tests verifying models, authentication, CRUD operations, and custom template filters:
```bash
python manage.py test potions
```
> **Result**: `Ran 20 tests — OK (All passed)`

---

## 🌐 Deploying to Vercel

MoodBrew is pre-configured for Vercel Serverless Python deployment using `@vercel/python`, `build_files.sh`, and WhiteNoise.

### Step 1: Push to GitHub
```bash
cd C:\Users\kotir\.gemini\antigravity\scratch\moodbrew
git remote add origin https://github.com/<YOUR-USERNAME>/moodbrew.git
git branch -M main
git push -u origin main
```

### Step 2: Import into Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your `moodbrew` repository.
3. Vercel automatically detects `vercel.json` and `build_files.sh`.
4. Click **Deploy**. Your app will be live on `https://<project-name>.vercel.app`!

> [!NOTE]
> On Vercel, `config/wsgi.py` automatically initializes the database in `/tmp` and runs migrations + seed data on cold starts, ensuring your deployed app is immediately usable.
