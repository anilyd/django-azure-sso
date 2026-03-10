## How Setup call call url on microsoft azure AD
Microsoft Azure Portal(https://portal.azure.com/)
1. App register
2. Search button :  App registrations

Display name :django-azure-login
Application (client) ID:3d5XXXXXXXXX
Object ID:627b6cXXXXXXXXXXXXXX
Directory (tenant) ID:0ba06b7bXXXXXXXXXXXXXXXXX
Supported account types:All Microsoft account users
Client credentials:0 certificate, 1 secret
Redirect URIs:1 web, 0 spa, 0 public client
Application ID URI:Add an Application ID URI
Managed application in local directory:Django-azure-login
State:Activated

# django-azure-ad-auth

Django app with Azure AD SSO login using custom User model.

## Features
- Azure AD / Microsoft login via MSAL
- Custom Django User model (email-based)
- Stores Azure OID, name, email from Microsoft Graph API
- Session-based authentication
- 

## Setup
1. Clone repo
2. pip install -r requirements.txt
3. Copy .env.example to .env and fill values
4. python manage.py migrate
5. python manage.py runserver

## Localhost url:

http://localhost:8000/accounts/login/


## Note: Below diagram will show properly on click edit button 


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



## Flow (Authentication Workflow)

User                Django              Azure AD           Graph API
 │                    │                    │                   │
 │─── GET /login/ ───▶│                    │                   │
 │◀── Login Page ─────│                    │                   │
 │                    │                    │                   │
 │─── Click "Sign     │                    │                   │
 │    in with MS" ───▶│                    │                   │
 │                    │──── Build Auth ────│                   │
 │                    │     URL (MSAL)     │                   │
 │◀── Redirect to ────│                    │                   │
 │    Microsoft ──────────────────────────▶│                   │
 │                    │                    │                   │
 │─── Enter Creds ───────────────────────▶│                   │
 │◀── Auth Code ──────────────────────────│                   │
 │    in Redirect ────────────────────────│                   │
 │                    │                   │                   │
 │─── GET /callback/ ▶│                   │                   │
 │    ?code=XXXX      │                   │                   │
 │                    │── Exchange Code ──▶│                   │
 │                    │◀─ Access Token ───│                   │
 │                    │                   │                   │
 │                    │── GET /v1.0/me ───────────────────────▶│
 │                    │◀─ User Profile ────────────────────────│
 │                    │  (email, name,    │                   │
 │                    │   azure_oid)      │                   │
 │                    │                   │                   │
 │                    │── Get or Create ──▶                   │
 │                    │   CustomUser DB   │                   │
 │                    │                   │                   │
 │◀── Redirect to ────│                   │                   │
 │    /home/ ─────────│                   │                   │
 │                    │                   │                   │


