#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("Installing google-api-python-client...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "google-api-python-client", "google-auth"])
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/drive"]
EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"
MIME_MD = "text/markdown"
MIME_GDOC = "application/vnd.google-apps.document"


def get_service():
    key_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    if not key_json:
        sys.exit("GOOGLE_SERVICE_ACCOUNT_KEY env var not set")
    info = json.loads(key_json)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def list_existing(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name)",
        pageSize=100,
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
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
            supportsAllDrives=True,
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
            supportsAllDrives=True,
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
        service.files().delete(fileId=existing[name], supportsAllDrives=True).execute()
        print(f"  Deleted stale: {name}")

    for f in md_files:
        upload_or_update(service, folder_id, f, existing)

    print("Done.")


if __name__ == "__main__":
    main()
