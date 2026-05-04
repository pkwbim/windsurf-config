---
name: sync-skill-to-hermes
description: "Sync the local agent-memex skill (or any skill in this repo) to the hermes runtime at hermes.apps.quanhox.com.tw, so the deployed agent picks up the latest version. Use when the user asks to push/update/deploy a skill to hermes, or whenever skill files under .windsurf/skills/ have just been edited and the user wants the change live for hermes."
---

# Sync Skill to Hermes

The hermes agent runtime lives on a separate server and reads skills from its own filesystem. After editing `.windsurf/skills/<name>/` here, the change must be rsynced to hermes for the deployed agent to see it.

## Connection (already provisioned)

Passwordless SSH from `dev2` to hermes is already set up in `~/.ssh/config`:

```
Host hermes
    HostName hermes.apps.quanhox.com.tw
    User hermes
```

Just `ssh hermes` works. If it ever asks for a password, the key was rotated — re-install `~/.ssh/id_ed25519.pub` into hermes's `~/.ssh/authorized_keys`.

## Path mapping

| Local (this repo) | Remote (hermes) |
|---|---|
| `.windsurf/skills/<name>/` | `/home/hermes/.hermes/profiles/little_flower/skills/productivity/<name>/` |

The remote layout uses a `productivity/` category folder. Other categories may exist (check with `ssh hermes 'ls /home/hermes/.hermes/profiles/little_flower/skills/'`); ask the user if you're unsure where a new skill belongs.

## Sync command

```bash
rsync -av --delete \
  .windsurf/skills/<skill-name>/ \
  hermes:/home/hermes/.hermes/profiles/little_flower/skills/productivity/<skill-name>/
```

- **Trailing slashes matter** on both source and destination — copies *contents into*, not the directory itself.
- `--delete` keeps remote in sync with local (removes files deleted locally). Omit it only if the user explicitly wants additive merge.
- Files land owned by `hermes:hermes` automatically because rsync runs as the hermes user.

## Verify

```bash
ssh hermes "ls -la /home/hermes/.hermes/profiles/little_flower/skills/productivity/<skill-name>/"
```

Confirm:
- All expected files present (especially `SKILL.md` and any `references/` subfiles)
- Owner is `hermes:hermes`
- Mtimes match what you just synced

## Common mistakes

- Forgetting trailing `/` on source → rsync copies the parent dir into the destination, creating a nested duplicate.
- Syncing without `--delete` after deleting a file locally → stale file lingers on hermes.
- Editing files directly on hermes → next sync from dev2 will overwrite them. Always edit in this repo, commit, then sync.

## Adjacent skills on hermes

`ls /home/hermes/.hermes/profiles/little_flower/skills/productivity/` may show extra skills hermes itself has authored (e.g. `agent-memex-asset-metadata`, `agent-memex-asset-workflow`). These are not in this repo. **Don't delete or overwrite them** unless the user asks — they belong to hermes's own iteration on top of the base skill.
