#!/usr/bin/env python3
"""Upload one file to Gilzone/gilzone.github.io using the stored custom.github credential."""
import sys, json, base64, urllib.request, urllib.error
from pathlib import Path

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

ALLOWED = ["api.github.com"]
OWNER, REPO = "Gilzone", "gilzone.github.io"
API = "https://api.github.com"

def api(method, path, data=None):
    req = urllib.request.Request(API + path, method=method,
        headers={"Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "User-Agent": "fish-single-upload"})
    dc.add_surrogate_to_request(req, "custom.github", entry_name="access_token", allowed_hosts=ALLOWED)
    body = json.dumps(data).encode() if data is not None else None
    try:
        resp = urllib.request.urlopen(req, data=body, timeout=30)
        return resp.status, dc.read_json_response(resp)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        return e.code, json.loads(raw) if raw.startswith("{") else {"raw": raw[:300]}

def main():
    local = Path(sys.argv[1]); rel = sys.argv[2]
    content = local.read_bytes()
    s, existing = api("GET", f"/repos/{OWNER}/{REPO}/contents/{rel}")
    sha = existing.get("sha") if s == 200 and isinstance(existing, dict) else None
    payload = {"message": f"Update {rel} — SUPERHOT low-poly restyle",
               "content": base64.b64encode(content).decode(),
               "branch": "main"}
    if sha: payload["sha"] = sha
    s, out = api("PUT", f"/repos/{OWNER}/{REPO}/contents/{rel}", payload)
    if s not in (200, 201):
        print("UPLOAD_FAILED", s, json.dumps(out)[:300]); return 1
    print("uploaded:", rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
