# 🥘 MasalaAI – Smart Kitchen Chef

A Flask web app that uses the **Gemini API** (key hidden on server) to generate quick recipes based on the user's available ingredients.

---

## 📁 Project Structure

```
masalaai/
├── app.py              ← Flask backend (API key lives here)
├── requirements.txt
├── templates/
│   └── index.html      ← Frontend (served by Flask)
└── README.md
```

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your Gemini API key

**Option A – Edit app.py directly (simple):**
Open `app.py` and replace:
```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
```
with your actual key:
```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIza...your_key...")
```

**Option B – Environment variable (recommended for deployment):**
```bash
export GEMINI_API_KEY="AIza...your_key..."
```
Or on Windows:
```bash
set GEMINI_API_KEY=AIza...your_key...
```

### 3. Run the server
```bash
python app.py
```
Visit: **http://localhost:5000**

---

## ☁️ Deploying (Render / Railway / Vercel)

Set the environment variable `GEMINI_API_KEY` in your hosting dashboard.
The key is **never exposed** to the browser — all Gemini calls happen server-side.

---

## ✨ Features
- 8 cuisine types (Indian, Chinese, Italian, Mexican, Continental, Indo-Chinese, Street Food, Surprise!)
- Type ingredients manually OR pick from a checklist
- Select available spices
- AI generates recipe with: Ingredients, Step-by-step cooking, Nutrition info, Substitution suggestions
- All recipes under 30 minutes
- Zero API key exposure to users
