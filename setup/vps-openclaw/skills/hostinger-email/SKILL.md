---
name: hostinger-email
description: List inbox and send email via Hostinger SMTP/IMAP. Use when Joshua asks to check mail, draft, or send.
user-invocable: true
---

# Hostinger email (SMTP/IMAP)

## Credentials

- Use process environment only: AGENT_EMAIL, AGENT_EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT, IMAP_HOST, IMAP_PORT.
- Never read ~/.openclaw/.env.
- Never print passwords or tokens in chat.

## Approval rules

- List inbox / summarize / draft: proceed.
- Send: show To, Subject, and body first. Only run send after Joshua says send it or approved.

## Commands (use exec)

Script path: {baseDir}/scripts/mail.py

List recent mail (subjects only):

    python3 {baseDir}/scripts/mail.py list --limit 10

Send mail (only after explicit approval):

    python3 {baseDir}/scripts/mail.py send --to "recipient@example.com" --subject "Your subject" --body "Your message body"

## Rules

- Prefer SMTP/IMAP via this skill. Do not use browser for email unless SMTP/IMAP fails.
- On auth or connection errors, report clearly and stop.
- Do not retry send without asking Joshua.
