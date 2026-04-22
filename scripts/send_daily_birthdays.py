#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, date
from zoneinfo import ZoneInfo
from urllib import request, parse

DATA_BIRTHDAYS = "data/aniversariantes.json"
DATA_LOG = "data/notification_log.json"
FORTALEZA_TZ = "America/Fortaleza"


def load_json(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def telegram_send_message(bot_token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    data = parse.urlencode(payload).encode("utf-8")

    req = request.Request(url, data=data, method="POST")
    with request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode("utf-8")
        if resp.status != 200:
            raise RuntimeError(f"Telegram HTTP {resp.status}: {body}")


def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("ERROR: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment.")
        sys.exit(1)

    now = datetime.now(ZoneInfo(FORTALEZA_TZ))
    today = now.date()
    today_str = today.isoformat()

    birthdays = load_json(DATA_BIRTHDAYS, default=[])
    log = load_json(DATA_LOG, default=[])

    sent_keys = {
        f"{entry.get('aniversariante_id')}|{entry.get('notified_date')}"
        for entry in log
    }

    active_birthdays = [person for person in birthdays if person.get("active", True) is True]

    todays_people = [
        person
        for person in active_birthdays
        if person.get("day") == today.day and person.get("month") == today.month
    ]
    # If not a leap year, birthdays on Feb 29 are notified on Feb 28
    if today.month == 2 and today.day == 28 and not is_leap_year(today.year):
        leap_people = [
            person
            for person in active_birthdays
            if person.get("day") == 29 and person.get("month") == 2
        ]
        todays_people.extend(leap_people)

    # Prevent sending the same notification more than once per day
    people_to_notify = []
    for person in todays_people:
        key = f"{person.get('id')}|{today_str}"
        if key not in sent_keys:
            people_to_notify.append(person)

    if not people_to_notify:
        return

    lines = []
    for person in people_to_notify:
        name = person.get("name", "").strip()
        description = person.get("description", "").strip()
        lines.append(f"• {name} — {description}")

    message = "🎉 Aniversariantes de hoje:\n\n" + "\n".join(lines)

    created_at = now.isoformat(timespec="seconds")

    # Save notification result to avoid duplicates in future runs
    try:
        telegram_send_message(bot_token, chat_id, message)

        for person in people_to_notify:
            log.append({
                "aniversariante_id": person.get("id"),
                "notified_date": today_str,
                "status": "SENT",
                "error_message": None,
                "created_at": created_at
            })

    except Exception as e:
        for person in people_to_notify:
            log.append({
                "aniversariante_id": person.get("id"),
                "notified_date": today_str,
                "status": "FAILED",
                "error_message": str(e),
                "created_at": created_at
            })

    save_json(DATA_LOG, log)


if __name__ == "__main__":
    main()