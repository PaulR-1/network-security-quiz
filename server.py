#!/usr/bin/env python3
"""Local server for the reviewers site and Cisco command practice.

Run from the repo root:

    python3 server.py

Saved commands are folders under cisco Command Practice/commands/.
"""

from __future__ import annotations

import html
import json
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRACTICE = ROOT / "cisco Command Practice"
COMMANDS = PRACTICE / "commands"
HOST = "0.0.0.0"
PORT = 43127
MAX_BODY = 20_000
USER_AGENT = "CiscoCommandPractice/1.0 (local study notebook)"

STACK_SITES = (
    ("networkengineering", "Network Engineering Stack Exchange", "https://networkengineering.stackexchange.com"),
    ("serverfault", "Server Fault", "https://serverfault.com"),
    ("superuser", "Super User", "https://superuser.com"),
)

STOP_WORDS = {
    "a",
    "an",
    "and",
    "cisco",
    "command",
    "for",
    "from",
    "in",
    "ios",
    "ip",
    "of",
    "on",
    "or",
    "show",
    "the",
    "to",
    "with",
}
EXPLAIN_MARKERS = (
    "used to",
    "displays",
    "lists ",
    "shows you",
    "show you",
    "status",
    "type ",
    "this command",
    "the command",
)
CONFIG_MARKERS = (
    "hostname ",
    "ip address",
    "no ip ",
    "interface vlan",
    "duplex ",
    "switchport ",
    "line vty",
    "ip routing",
    "yes nvram",
    "up down",
)
DRIFT_MARKERS = (
    "reload",
    "configure terminal",
    "copy running",
    "write memory",
    "enable secret",
)

WRITE_LOCK = threading.Lock()
SEARCH_CACHE: dict[str, tuple[float, list[dict[str, str]]]] = {}
CACHE_SECONDS = 600


class PracticeError(Exception):
    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.status = status


def clean_text(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = html.unescape(text).replace("\xa0", " ")
    text = text.replace("\u2026", "...")
    return re.sub(r"\s+", " ", text).strip()


def collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def slugify(command: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", command.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)[:60].strip("-")
    return slug


def command_tokens(command: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", command.lower())
    tokens = [word for word in words if word not in STOP_WORDS and len(word) > 1]
    return tokens or [word for word in words if len(word) > 1]


def has_marker(blob: str, marker: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(marker.strip()) + r"(?![a-z0-9])", blob) is not None


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("-", " ")).strip()


def mentions_command(command: str, text: str) -> bool:
    phrase = normalized(command)
    return bool(phrase) and phrase in normalized(text)


def repair_command(command: str, text: str) -> str:
    if "-" not in command:
        return text
    spaced = re.sub(r"\s*-\s*", " - ", command.strip())
    return re.sub(re.escape(spaced), command.strip(), text, flags=re.IGNORECASE)


def score_note(command: str, title: str, text: str) -> int:
    blob = f"{title} {text}".lower()
    score = 5 if mentions_command(command, blob) else 0
    score += sum(2 for token in command_tokens(command) if re.search(r"(?<![a-z0-9])" + re.escape(token) + r"(?![a-z0-9])", blob))
    explained = sum(2 for marker in EXPLAIN_MARKERS if marker in blob)
    score += explained
    if explained == 0:
        score -= 5
    score -= sum(4 for marker in CONFIG_MARKERS if has_marker(blob, marker))
    if "codes:" in blob or "c - connected" in blob or "----" in text:
        score -= 6
    return score


def tidy_excerpt(text: str) -> str:
    text = re.split(r"\s+[–—]\s+", text, maxsplit=1)[0]
    text = text.replace("...", " ... ")
    text = re.sub(r"\s+", " ", text).strip(" -")

    def collapse_quotes(match: re.Match[str]) -> str:
        inner = re.sub(r"\s+", " ", match.group(1)).strip()
        return f'"{inner}"'

    return re.sub(r'"([^"]*)"', collapse_quotes, text)


def best_excerpt(command: str, text: str) -> tuple[str, int]:
    pieces = [piece.strip(" -") for piece in re.split(r"\s+\.\.\.\s+", tidy_excerpt(text)) if piece.strip(" -")]
    windows: list[str] = []
    for index, piece in enumerate(pieces):
        windows.append(piece)
        if index + 1 >= len(pieces):
            continue
        follow = pieces[index + 1]
        follow_low = follow.lower()
        explains = any(marker in follow_low for marker in EXPLAIN_MARKERS)
        drifts = any(marker in follow_low for marker in DRIFT_MARKERS)
        if explains and not drifts:
            windows.append(f"{piece} {follow}")
    if not windows:
        windows = [tidy_excerpt(text)]
    ranked = []
    for window in windows:
        window = repair_command(command, window)
        if len(window) < 40 or not mentions_command(command, window):
            continue
        ranked.append((score_note(command, "", window), clip(window, 360)))
    if not ranked:
        cleaned = clip(tidy_excerpt(text), 360)
        return cleaned, score_note(command, "", cleaned)
    ranked.sort(key=lambda item: (item[0], -len(item[1])), reverse=True)
    return ranked[0][1], ranked[0][0]


def clip(text: str, limit: int = 420) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return f"{cut}..."


def fetch_json(url: str, timeout: int = 12) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read()
        if response.headers.get("Content-Encoding") == "gzip":
            import gzip

            raw = gzip.decompress(raw)
        return json.loads(raw.decode("utf-8"))


def stack_notes(site: str, label: str, origin: str, command: str) -> list[dict[str, str]]:
    params = urllib.parse.urlencode(
        {
            "order": "desc",
            "sort": "relevance",
            "q": f"{command} cisco ios",
            "site": site,
            "pagesize": 8,
        }
    )
    payload = fetch_json(f"https://api.stackexchange.com/2.3/search/excerpts?{params}")
    notes: list[dict[str, str]] = []
    for item in payload.get("items", []):
        title = clean_text(item.get("title") or "Cisco command note")
        text, ranked = best_excerpt(command, clean_text(item.get("excerpt") or ""))
        if len(text) < 40 or ranked < 6 or not mentions_command(command, text):
            continue
        if item.get("answer_id"):
            link = f"{origin}/a/{item['answer_id']}"
        elif item.get("question_id"):
            link = f"{origin}/questions/{item['question_id']}"
        else:
            continue
        notes.append(
            {
                "title": title,
                "source": label,
                "link": link,
                "text": text,
                "score": str(ranked),
            }
        )
    return notes


def wiki_notes(command: str) -> list[dict[str, str]]:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": f"{command} Cisco IOS",
            "srlimit": 3,
            "utf8": 1,
            "format": "json",
        }
    )
    payload = fetch_json(f"https://en.wikipedia.org/w/api.php?{params}")
    hits = payload.get("query", {}).get("search", [])
    notes: list[dict[str, str]] = []
    for hit in hits:
        title = clean_text(hit.get("title") or "")
        snippet = clip(clean_text(hit.get("snippet") or ""))
        ranked = score_note(command, title, snippet)
        if ranked < 6 or not title:
            continue
        extract_params = urllib.parse.urlencode(
            {
                "action": "query",
                "prop": "extracts",
                "exintro": 1,
                "explaintext": 1,
                "exchars": 420,
                "titles": title,
                "format": "json",
            }
        )
        extract_payload = fetch_json(f"https://en.wikipedia.org/w/api.php?{extract_params}")
        pages = extract_payload.get("query", {}).get("pages", {})
        extract = ""
        for page in pages.values():
            extract = clip(clean_text(page.get("extract") or ""))
        text = extract if mentions_command(command, extract) else snippet
        if len(text) < 40 or not mentions_command(command, text):
            continue
        notes.append(
            {
                "title": title,
                "source": "Wikipedia",
                "link": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                "text": text,
                "score": str(max(ranked, score_note(command, title, text))),
            }
        )
    return notes


def search_web(command: str) -> list[dict[str, str]]:
    key = collapse(command).lower()
    cached = SEARCH_CACHE.get(key)
    now = time.time()
    if cached and now - cached[0] < CACHE_SECONDS:
        return cached[1]

    notes: list[dict[str, str]] = []
    failures = 0
    attempts = 0
    for site, label, origin in STACK_SITES:
        attempts += 1
        try:
            notes.extend(stack_notes(site, label, origin, command))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
            failures += 1
        if len(notes) >= 8:
            break
    if len(notes) < 4:
        attempts += 1
        try:
            notes.extend(wiki_notes(command))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
            failures += 1
    if not notes and failures == attempts:
        raise PracticeError("The search did not respond. Try again in a moment.", 502)

    unique: list[dict[str, str]] = []
    seen: set[str] = set()
    for note in sorted(notes, key=lambda item: int(item["score"]), reverse=True):
        marker = note["link"]
        fingerprint = note["text"][:160].lower()
        if marker in seen or fingerprint in seen:
            continue
        seen.add(marker)
        seen.add(fingerprint)
        unique.append({key: note[key] for key in ("title", "source", "link", "text")})
    SEARCH_CACHE[key] = (now, unique)
    return unique


def validate_command(command: str) -> str:
    command = collapse(command)
    if not command:
        raise PracticeError("Type a command first.")
    if len(command) > 200:
        raise PracticeError("That command is too long.")
    if any(ord(char) < 32 for char in command):
        raise PracticeError("The command has characters that cannot be saved.")
    if not slugify(command):
        raise PracticeError("Use letters or numbers in the command.")
    return command


def validate_description(description: str) -> str:
    description = collapse(description)
    if not description:
        raise PracticeError("Write a description first.")
    if len(description) > 2000:
        raise PracticeError("That description is too long.")
    return description


def same_command(left: str, right: str) -> bool:
    return collapse(left).lower() == collapse(right).lower()


def folder_for(command: str) -> tuple[Path, bool]:
    base = slugify(command)
    COMMANDS.mkdir(parents=True, exist_ok=True)
    for index in range(1, 60):
        slug = base if index == 1 else f"{base}-{index}"
        path = (COMMANDS / slug).resolve()
        if path.parent != COMMANDS.resolve():
            raise PracticeError("That command cannot be saved.")
        if not path.exists():
            return path, True
        stored = (path / "command.txt").read_text(encoding="utf-8")
        if same_command(stored, command):
            return path, False
    raise PracticeError("Too many folders use that command name.")


def read_web_note(path: Path) -> dict[str, str] | None:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return None
    header, _, body = raw.partition("\n\n")
    fields: dict[str, str] = {}
    for line in header.splitlines():
        if ": " not in line:
            return {"kind": "yours", "text": raw}
        name, value = line.split(": ", 1)
        fields[name.strip().lower()] = value.strip()
    if "link" not in fields:
        return {"kind": "yours", "text": raw}
    return {
        "kind": "web",
        "title": fields.get("title") or "Web note",
        "source": fields.get("source") or "Web",
        "link": fields["link"],
        "text": body.strip() or fields.get("title") or "",
    }


def description_order(path: Path) -> tuple:
    name = path.name
    if name == "description.txt":
        return (0, 0, name)
    numbered = re.fullmatch(r"description-(\d+)\.txt", name)
    if numbered:
        return (0, int(numbered.group(1)), name)
    web = re.fullmatch(r"web-(\d+)\.txt", name)
    if web:
        return (1, int(web.group(1)), name)
    return (2, 0, name)


def read_entry(path: Path) -> dict:
    command = (path / "command.txt").read_text(encoding="utf-8").strip()
    descriptions = []
    files = sorted(path.iterdir(), key=description_order)
    for child in files:
        if not child.is_file() or child.name == "command.txt" or child.name.startswith("."):
            continue
        if child.name.startswith("web-"):
            note = read_web_note(child)
            if note:
                descriptions.append(note)
            continue
        text = child.read_text(encoding="utf-8").strip()
        if text:
            descriptions.append({"kind": "yours", "text": text})
    return {"slug": path.name, "command": command, "descriptions": descriptions}


def list_entries() -> list[dict]:
    if not COMMANDS.exists():
        return []
    entries = []
    for path in sorted(COMMANDS.iterdir(), key=lambda item: item.name):
        if path.is_dir() and (path / "command.txt").is_file():
            entries.append(read_entry(path))
    entries.sort(key=lambda item: item["command"].lower())
    return entries


def next_numbered(path: Path, prefix: str, start: int = 1) -> Path:
    number = start
    while (path / f"{prefix}-{number}.txt").exists():
        number += 1
        if number > 30:
            raise PracticeError("This folder already has plenty of notes.")
    return path / f"{prefix}-{number}.txt"


def save_command(command: str, description: str) -> dict:
    command = validate_command(command)
    description = validate_description(description)
    with WRITE_LOCK:
        path, created = folder_for(command)
        path.mkdir(parents=True, exist_ok=True)
        if created:
            (path / "command.txt").write_text(command + "\n", encoding="utf-8")
            (path / "description.txt").write_text(description + "\n", encoding="utf-8")
        else:
            target = next_numbered(path, "description", start=2)
            target.write_text(description + "\n", encoding="utf-8")
        entry = read_entry(path)
    return {"created": created, "entry": entry}


def saved_links(path: Path) -> set[str]:
    links = set()
    for child in path.glob("web-*.txt"):
        note = read_web_note(child)
        if note and note.get("link"):
            links.add(note["link"])
    return links


def add_web_descriptions(slug: str) -> dict:
    if not re.fullmatch(r"[a-z0-9-]{1,80}", slug or ""):
        raise PracticeError("That folder was not found.", 404)
    path = (COMMANDS / slug).resolve()
    if path.parent != COMMANDS.resolve() or not (path / "command.txt").is_file():
        raise PracticeError("That folder was not found.", 404)
    command = (path / "command.txt").read_text(encoding="utf-8").strip()
    found = search_web(command)
    with WRITE_LOCK:
        existing = saved_links(path)
        added = 0
        for note in found:
            if note["link"] in existing:
                continue
            if added >= 3:
                break
            target = next_numbered(path, "web")
            body = (
                f"Source: {note['source']}\n"
                f"Link: {note['link']}\n"
                f"Title: {note['title']}\n"
                f"\n"
                f"{note['text']}\n"
            )
            target.write_text(body, encoding="utf-8")
            existing.add(note["link"])
            added += 1
        entry = read_entry(path)
    if added:
        message = f"Added {added} description{'s' if added != 1 else ''} from the web."
    elif found:
        message = "Those descriptions are already in this folder."
    else:
        message = "No extra descriptions turned up for that command."
    return {"added": added, "message": message, "entry": entry}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/commands":
            self.respond(200, {"commands": list_entries()})
            return
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        try:
            payload = self.read_json()
            if parsed.path == "/api/commands":
                result = save_command(str(payload.get("command", "")), str(payload.get("description", "")))
                self.respond(200, result)
                return
            if parsed.path == "/api/commands/search":
                result = add_web_descriptions(str(payload.get("slug", "")))
                self.respond(200, result)
                return
            self.respond(404, {"error": "That action was not found."})
        except PracticeError as exc:
            self.respond(exc.status, {"error": str(exc)})
        except json.JSONDecodeError:
            self.respond(400, {"error": "The request was not valid."})

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length < 0 or length > MAX_BODY:
            raise PracticeError("That note is too large.")
        raw = self.rfile.read(length)
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise PracticeError("The request was not valid.")
        return data

    def respond(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")


def main() -> None:
    COMMANDS.mkdir(parents=True, exist_ok=True)
    ThreadingHTTPServer.allow_reuse_address = True
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Reviewers: http://127.0.0.1:{PORT}/")
    print(f"Cisco command practice: http://127.0.0.1:{PORT}/cisco%20Command%20Practice/")
    server.serve_forever()


if __name__ == "__main__":
    main()
