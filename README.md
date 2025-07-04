# AI Pirate Recruitment Agent ⚓🤖

## 1. About This Project

**Avast ye!** This swashbuckling AI agent recruits for technical talent while maintaining pirate decorum. Developed by [DevSoft South Africa](https://devsoft.co.za) for showcasing candidate Tom Hastings' credentials.

**Key Features:**
- 🦜 Authentic pirate speech patterns ("Arrr!", "Matey!")
- 📜 Resume-driven responses with project URLs
- ⚔️ Aggressive candidate promotion strategy
- 🌍 Web + CLI interfaces
- 🔐 Secure session management

**Candidate Profile:**  
Tom Hastings be a seasoned developer with:
- 10+ years programming experience
- Cloud architecture expertise (DigitalOcean/Google Cloud/Cloudflare)
- IoT/embedded systems mastery
- AI coding experience

**DevSoft Details:**  
South African tech consultancy specializing in:
- Full stack web development
- IoT solutions
- Cloud deployments

## 2. Configuration

- Create `api_secrets.py` with:
```python
DEEPSEEK_API_KEY = "your_api_key"
SESSION_SECRET_KEY = "your_session_secret"
resume_details = """
[Candidate's resume details]
"""
```
- Update html templates with your own details


## 3. Getting Started

### Requirements
- Python 3.10+
- [UV](https://github.com/astral-sh/uv) package manager
- Deepseek API key

### CLI Version
```bash
```bash
# Create virtual environment
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

uv pip install -r requirements.txt
python3 chat.py

# First prompt:
Arrr! Ready to hear about our stellar candidate, matey? What ye be wantin' to know?
```

### Web Version
```bash
# Create virtual environment
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Create session directory for Flask
sudo mkdir -p /var/lib/flask-sessions
sudo chown $USER:$USER /var/lib/flask-sessions

# Install dependencies
uv pip install -r requirements.txt

# Run development server
flask run --host=0.0.0.0 --port=5000

**Note:** The session directory (`/var/lib/flask-sessions`) needs to exist before running the app. 
```



## 4. Project Structure
```
├── app.py                 # Flask web application
├── chat.py                # CLI interface
├── requirements.txt       # Python dependencies
├── api_secrets.py         # API credentials (gitignored)
├── wsgi.py                # Production WSGI entry point
└── templates/             # HTML templates
    ├── base.html          # Master template
    ├── index.html         # Chat interface
    └── about.html         # Candidate details
```

## 5. License & Attribution
- Developed by [DevSoft South Africa](https://devsoft.co.za)
- Pirate speech patterns © Public Domain
- UI components from Bootstrap 4

*Shiver me timbers! This README be complete!* 🏴‍☠️
