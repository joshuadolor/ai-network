#!/usr/bin/env python3
"""Hostinger mail via SMTP/IMAP — reads credentials from environment only."""

import argparse
import email
import imaplib
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def env(name: str, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if not val:
        print(f"Missing env: {name}", file=sys.stderr)
        sys.exit(1)
    return val


def smtp_send(to_addr: str, subject: str, body: str) -> None:
    user = env("AGENT_EMAIL")
    password = env("AGENT_EMAIL_PASSWORD")
    host = env("SMTP_HOST", "smtp.hostinger.com")
    port = int(env("SMTP_PORT", "587"))

    msg = MIMEMultipart()
    msg["From"] = user
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(host, port, timeout=60) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, [to_addr], msg.as_string())

    print(f"Sent to {to_addr} | Subject: {subject}")


def imap_list(limit: int) -> None:
    user = env("AGENT_EMAIL")
    password = env("AGENT_EMAIL_PASSWORD")
    host = env("IMAP_HOST", "imap.hostinger.com")
    port = int(env("IMAP_PORT", "993"))

    with imaplib.IMAP4_SSL(host, port) as imap:
        imap.login(user, password)
        imap.select("INBOX")
        _, data = imap.search(None, "ALL")
        ids = data[0].split()
        if not ids:
            print("Inbox is empty.")
            return

        for num in ids[-limit:]:
            _, msg_data = imap.fetch(num, "(RFC822)")
            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)
            subj = msg.get("Subject", "(no subject)")
            sender = msg.get("From", "(unknown)")
            print(f"- From: {sender} | Subject: {subj}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hostinger email helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List recent inbox messages")
    p_list.add_argument("--limit", type=int, default=10)

    p_send = sub.add_parser("send", help="Send an email")
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--subject", required=True)
    p_send.add_argument("--body", required=True)

    args = parser.parse_args()

    if args.cmd == "list":
        imap_list(args.limit)
    elif args.cmd == "send":
        smtp_send(args.to, args.subject, args.body)


if __name__ == "__main__":
    main()
