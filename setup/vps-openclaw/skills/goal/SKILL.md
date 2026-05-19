---
name: goal
description: Manage goals from Discord using /goal-style commands. Creates goal records, tracks progress, and keeps status visible to Joshua.
user-invocable: true
---

# Goal skill (`/goal`)

Use this whenever Joshua sends commands like:

- `/goal launch ...`
- `/goal update ...`
- `/goal done ...`
- `/goal list`
- `/goal status ...`

This skill gives Felix a deterministic workflow so goals are not lost in chat.

## Strict mode (mandatory)

When a goal is `active`, Felix must keep executing toward that goal and **must not stop** unless one of these is true:

1. Goal is completed → mark `done`.
2. Goal is blocked by an external dependency or approval that Felix cannot bypass.

No other “pause”, “later”, or silent stop is allowed while a goal is active.

If blocked, Felix must post:

```text
🛑 Goal blocked: <id> <title>
Reason: <specific blocker>
Needs from Joshua: <single clear unblock action>
```

Then record:

```bash
python3 {baseDir}/scripts/goal_tracker.py update <id> --status blocked --note "<reason>"
```

## Command mapping

### 1) Start a goal

Input examples:

- `/goal launch Build website trial pipeline`
- `/goal start Build website trial pipeline`

Action:

```bash
python3 {baseDir}/scripts/goal_tracker.py start "Build website trial pipeline" \
  --success "Trial lead -> draft site -> ngrok preview sent" \
  --next "Gather 3 leads without websites" \
  --next "Draft first landing page"
```

Then reply in Discord:

```text
🎯 Goal started: <title>
ID: <id>
Next:
- ...
- ...
```

Immediately start **ralph-loop** for execution tracking:

```bash
python3 ~/.openclaw/workspace/skills/ralph-loop/scripts/ralph_status.py start "Goal <id>: <title>"
```

### 2) Update a goal

Input examples:

- `/goal update ab12cd34 blocked waiting for checkpoint`
- `/goal status ab12cd34 in progress`

Action:

```bash
python3 {baseDir}/scripts/goal_tracker.py update ab12cd34 \
  --status blocked \
  --note "waiting for checkpoint on KUBB"
```

### 3) Complete a goal

Input:

- `/goal done ab12cd34`

Action:

```bash
python3 {baseDir}/scripts/goal_tracker.py done ab12cd34 --note "completed"
```

### 4) List goals

Input:

- `/goal list`

Action:

```bash
python3 {baseDir}/scripts/goal_tracker.py list
```

## Execution contract for active goals

After `/goal start|launch`, Felix should run this cycle until `done` or `blocked`:

1. Choose next action from goal + context.
2. Execute with tools/skills.
3. Update goal note:

   ```bash
   python3 {baseDir}/scripts/goal_tracker.py update <id> --note "<what changed>"
   ```

4. Use **ralph-loop** ping checks every ~5 min.
5. Repeat.

Never leave an active goal without either:

- `python3 {baseDir}/scripts/goal_tracker.py done <id> ...`
- or `--status blocked` with explicit unblock request to Joshua.

## Storage

- Index: `~/.openclaw/workspace/docs/goals/goals.json`
- Per-goal note: `~/.openclaw/workspace/docs/goals/<id>-<slug>.md`

## Rules

- Always use the script; do not maintain ad-hoc goal memory in chat only.
- For long goals, also use skill **ralph-loop** (5-minute progress pings).
- If user text is ambiguous, ask one short clarification before creating/updating.
- Active goal = strict continuity until `done` or `blocked`.
