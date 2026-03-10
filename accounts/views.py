import msal
import requests
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

### Helper function to create MSAL app instance: Be Focused on this part when debugging authentication issues! ###
def get_msal_app():
    return msal.ConfidentialClientApplication(
        settings.AZURE_AD["CLIENT_ID"],
        authority=f"https://login.microsoftonline.com/{settings.AZURE_AD['TENANT_ID']}",
        client_credential=settings.AZURE_AD["CLIENT_SECRET"],
    )




# def get_msal_app():
#     return msal.ConfidentialClientApplication(
#         settings.AZURE_AD["CLIENT_ID"],
#         authority="https://login.microsoftonline.com/organizations",  # ✅ Fix
#         client_credential=settings.AZURE_AD["CLIENT_SECRET"],
#     )
    
# def get_msal_app():
#     return msal.ConfidentialClientApplication(
#         settings.AZURE_AD["CLIENT_ID"],
#         authority=f"https://login.microsoftonline.com/{settings.AZURE_AD['TENANT_ID']}",  # ✅ Tenant-specific
#         client_credential=settings.AZURE_AD["CLIENT_SECRET"],
#     )

# def get_msal_app():
#     return msal.ConfidentialClientApplication(
#         settings.AZURE_AD["CLIENT_ID"],
#         authority="https://login.microsoftonline.com/consumers",  # ✅ For personal accounts
#         client_credential=settings.AZURE_AD["CLIENT_SECRET"],
#     )


# def get_msal_app():
#     return msal.ConfidentialClientApplication(
#         settings.AZURE_AD["CLIENT_ID"],
#         authority="https://login.microsoftonline.com/common",  # ✅ Supports all account types
#         client_credential=settings.AZURE_AD["CLIENT_SECRET"],
#     )


def azure_login(request):
    """Redirect user to Azure AD login page."""
    msal_app = get_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=settings.AZURE_AD["SCOPES"],
        redirect_uri=settings.AZURE_AD["REDIRECT_URI"],
    )
    return redirect(auth_url)


def azure_callback(request):
    """Handle callback from Azure AD after login."""
    code = request.GET.get("code")
    if not code:
        return render(request, "accounts/login.html", {"error": "Login failed. No code received."})

    msal_app = get_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=settings.AZURE_AD["SCOPES"],
        redirect_uri=settings.AZURE_AD["REDIRECT_URI"],
    )

    if "error" in result:
        return render(request, "accounts/login.html", {
            "error": result.get("error_description", "Authentication failed.")
        })

    # Get user info from Microsoft Graph API
    access_token = result.get("access_token")
    graph_response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile = graph_response.json()

    # Get or create user in DB
    from accounts.models import CustomUser

    azure_oid = profile.get("id")
    email = profile.get("mail") or profile.get("userPrincipalName", "")
    first_name = profile.get("givenName", "")
    last_name = profile.get("surname", "")

    user, created = CustomUser.objects.get_or_create(
        azure_oid=azure_oid,
        defaults={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        },
    )

    if not created:
        # Update info on each login
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect("home")


def azure_logout(request):
    logout(request)
    return redirect("login_page")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "accounts/login.html")


@login_required
def home(request):
    return render(request, "home.html")