
# Blotato Clone – Automated Python Social Media Posting System

This is a full-featured backend system inspired by [blotato.com](https://blotato.com) that allows users to:

✅ Connect their Facebook, Instagram, YouTube, and TikTok accounts  
✅ Securely store tokens using AES encryption  
✅ Upload content and publish across all platforms from one UI  
✅ Integrate automated workflows using **n8n**

---

## 🚀 Features

- ✅ OAuth login for Facebook, Instagram, YouTube, TikTok
- ✅ Secure token encryption using Fernet (AES)
- ✅ SQLite or PostgreSQL storage via SQLModel
- ✅ Dashboard UI (HTML + Jinja2)
- ✅ Unified `/dashboard/post` route for mass publishing
- ✅ Works with `n8n` via webhook automation
- ✅ Deployable to Railway, Render, Docker

---

## 🧰 Tech Stack

- Python 3.11+
- FastAPI + SQLModel
- Jinja2 Templates
- aiohttp for async media upload
- authlib for OAuth2 integrations
- cryptography for token encryption

---

## 📦 Installation

1. **Clone the repo:**

```bash
git clone https://github.com/yourname/blotato-clone.git
cd blotato-clone
```

2. **Create virtual environment:**

```bash
python -m venv venv && source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure `.env`:**

```env
ENCRYPTION_KEY=generate_this_using_fernet
DATABASE_URL=sqlite:///./blotato.db

FB_CLIENT_ID=your_facebook_id
FB_CLIENT_SECRET=your_facebook_secret

GOOGLE_CLIENT_ID=your_google_id
GOOGLE_CLIENT_SECRET=your_google_secret

TIKTOK_CLIENT_ID=your_tiktok_id
TIKTOK_CLIENT_SECRET=your_tiktok_secret

BASE_URL=http://localhost:8080
```

To generate an encryption key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

5. **Start the server:**

```bash
uvicorn main:app --reload --port 8080
```

---

## 🧑‍🎨 Dashboard UI

Visit:

```
http://localhost:8080/dashboard
```

From there, you can:

- Connect each platform account
- Upload a post (text + media)
- Trigger cross-platform publishing

---

## 🔁 n8n Integration (Optional Automation)

1. Import `n8n_auto_post_workflow.json` into your n8n instance.
2. Trigger it via cron/schedule, webhook, or external tool.
3. It will `POST` to `/dashboard/post` with required fields.

---

## 🐳 Optional Docker Usage

```bash
docker build -t blotato-backend .
docker run -p 8080:8080 --env-file .env blotato-backend
```

---

## 🛠 TODO / Future Enhancements

- Add webhook listeners for post success/failure
- Support multiple media files (IG Carousel)
- Add post scheduling UI
- Dashboard analytics per platform

---

## 📄 License

MIT – Use freely and modify for commercial or personal use.
