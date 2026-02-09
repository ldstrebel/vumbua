#!/usr/bin/env python3
"""
One-time setup script. Run this locally to get a Google OAuth refresh token
for the GitHub Action to use.

Prerequisites:
  pip install google-auth-oauthlib

Usage:
  python scripts/get_refresh_token.py <CLIENT_ID> <CLIENT_SECRET>

It will open a browser for you to sign in with your Google account.
After authorization, it prints the refresh token to add as a GitHub secret.
"""
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/get_refresh_token.py <CLIENT_ID> <CLIENT_SECRET>")
        sys.exit(1)

    client_id = sys.argv[1]
    client_secret = sys.argv[2]

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

    print("\n" + "=" * 60)
    print("SUCCESS! Add these as GitHub repo secrets:")
    print("=" * 60)
    print(f"\nGOOGLE_CLIENT_ID = {client_id}")
    print(f"GOOGLE_CLIENT_SECRET = {client_secret}")
    print(f"GOOGLE_REFRESH_TOKEN = {creds.refresh_token}")
    print("\nGo to: https://github.com/ldstrebel/vumbua/settings/secrets/actions")
    print("=" * 60)


if __name__ == "__main__":
    main()
