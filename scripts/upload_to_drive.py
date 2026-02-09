#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"
MIME_MD = "text/markdown"


def get_service():
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        sys.exit(
            "Missing env vars. Need: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN"
        )

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/drive.file"],
    )
    creds.refresh(Request())
    return build("drive", "v3", credentials=creds)


def list_existing(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name)",
        pageSize=100,
    ).execute()
    return {f["name"]: f["id"] for f in results.get("files", [])}


def upload_or_update(service, folder_id, local_path, existing_files):
    name = local_path.name
    media = MediaFileUpload(str(local_path), mimetype=MIME_MD, resumable=True)

    if name in existing_files:
        file_id = existing_files[name]
        service.files().update(
            fileId=file_id,
            media_body=media,
        ).execute()
        print(f"  Updated: {name}")
    else:
        metadata = {
            "name": name,
            "parents": [folder_id],
        }
        service.files().create(
            body=metadata,
            media_body=media,
            fields="id",
        ).execute()
        print(f"  Created: {name}")


def main():
    folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    if not folder_id:
        sys.exit("GOOGLE_DRIVE_FOLDER_ID env var not set")

    if not EXPORTS_DIR.exists():
        sys.exit(f"Exports directory not found: {EXPORTS_DIR}")

    md_files = sorted(EXPORTS_DIR.glob("*.md"))
    if not md_files:
        sys.exit("No .md files found in exports/")

    print(f"Uploading {len(md_files)} files to Drive folder {folder_id}...")
    service = get_service()
    existing = list_existing(service, folder_id)

    stale = set(existing.keys()) - {f.name for f in md_files}
    for name in stale:
        service.files().delete(fileId=existing[name]).execute()
        print(f"  Deleted stale: {name}")

    for f in md_files:
        upload_or_update(service, folder_id, f, existing)

    print("Done.")


if __name__ == "__main__":
    main()
