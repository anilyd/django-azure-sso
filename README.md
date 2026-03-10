# django-azure-ad-auth

Django app with Azure AD SSO login using custom User model.

## Features
- Azure AD / Microsoft login via MSAL
- Custom Django User model (email-based)
- Stores Azure OID, name, email from Microsoft Graph API
- Session-based authentication

## Setup
1. Clone repo
2. pip install -r requirements.txt
3. Copy .env.example to .env and fill values
4. python manage.py migrate
5. python manage.py runserver


## 🏗️ System Design

┌─────────────────────────────────────────────────────────┐
│                     CLIENT BROWSER                       │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP Request
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   DJANGO APPLICATION                     │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐   ┌─────────────┐  │
│  │  accounts/  │    │  accounts/  │   │  accounts/  │  │
│  │  urls.py    │───▶│  views.py   │──▶│  models.py  │  │
│  └─────────────┘    └──────┬──────┘   └─────────────┘  │
│                            │                CustomUser   │
│                            │ MSAL Library               │
└────────────────────────────┼────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
   ┌─────────────────┐  ┌────────┐  ┌─────────────────┐
   │  Azure AD /     │  │ SQLite │  │  Microsoft      │
   │  Microsoft      │  │   DB   │  │  Graph API      │
   │  Login Server   │  └────────┘  │  /v1.0/me       │
   └─────────────────┘              └─────────────────┘
