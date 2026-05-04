---
name: sync-skill-to-hermes
description: "Sync a skill from any project's .windsurf/skills/ directory on dev2 to the hermes runtime at hermes.apps.quanhox.com.tw, so the deployed agent picks up the change. Use when the user asks to push/update/deploy a skill to hermes, or whenever a SKILL.md / references/ file has just been edited and needs to go live."
---

# Sync Skill to Hermes

The hermes agent runtime lives on a separate server (`hermes.apps.quanhox.com.tw`) and reads skills from its own filesystem. dev2 is where skills are authored — after editing `.windsurf/skills/<name>/` in any project, the change must be rsynced to hermes for the deployed agent to see it.

This skill applies regardless of which project on dev2 you're editing in (`agent-memex`, `wp-manager`, `task-agent-api`, `db-manager`, etc.). All of them share the same windsurf-config submodule and rsync to the same hermes target.

## Connection (already provisioned)

Passwordless SSH from `dev2` to hermes is already set up in `~/.ssh/config`:

```
Host hermes
    HostName hermes.apps.quanhox.com.tw
    User hermes
```

Just `ssh hermes` works. If it ever asks for a password, the key was rotated — re-install `~/.ssh/id_ed25519.pub` into hermes's `~/.ssh/authorized_keys`.

## Path mapping

| Local (any project on dev2) | Remote (hermes) |
|---|---|
| `<project>/.windsurf/skills/<name>/` | `/home/hermes/.hermes/profiles/little_flower/skills/<category>/<name>/` |

`<category>` is usually `productivity/`. Other categories may exist — check with:

```bash
ssh hermes 'ls /home/hermes/.hermes/profiles/little_flower/skills/'
```

If the skill is new and you're not sure which category, ask the user.

## Sync command

From the project root that contains the skill:

```bash
rsync -av --delete \
  .windsurf/skills/<skill-name>/ \
  hermes:/home/hermes/.hermes/profiles/little_flower/skills/<category>/<skill-name>/
```

- **Trailing slashes matter** on both source and destination — copies *contents into*, not the directory itself.
- `--delete` keeps remote in sync with local (removes files deleted locally). Omit it only if the user explicitly wants additive merge.
- Files land owned by `hermes:hermes` automatically because rsync runs as the hermes user.

## Verify

```bash
ssh hermes "ls -la /home/hermes/.hermes/profiles/little_flower/skills/<category>/<skill-name>/"
```

Confirm:
- All expected files present (especially `SKILL.md` and any `references/` subfiles)
- Owner is `hermes:hermes`
- Mtimes match what you just synced

## Source-of-truth note

Skills live in `pkwbim/windsurf-config` (a GitHub repo) and are pulled into each dev2 project as a `.windsurf/` submodule. The canonical edit flow:

1. Edit in any project's `.windsurf/skills/<name>/`
2. Commit + push inside the submodule (`cd .windsurf && git add … && git commit && git push`)
3. (Optional) Update the parent project's submodule pointer
4. **Rsync to hermes** ← this skill

Other dev2 projects can refresh their submodule with `git submodule update --remote .windsurf` to pull the latest skills.

## Common mistakes

- Forgetting trailing `/` on source → rsync copies the parent dir into the destination, creating a nested duplicate.
- Syncing without `--delete` after deleting a file locally → stale file lingers on hermes.
- Editing files directly on hermes → next sync from dev2 will overwrite them. Always edit in dev2, commit, then sync.
- Forgetting to push the windsurf submodule to GitHub before sync → other projects won't see the change later.

## Adjacent skills on hermes

`ls /home/hermes/.hermes/profiles/little_flower/skills/productivity/` may show extra skills hermes itself has authored (e.g. `agent-memex-asset-metadata`, `agent-memex-asset-workflow`). These are **not** in any dev2 project's repo. **Don't delete or overwrite them** unless the user asks — they belong to hermes's own iteration on top of the base skill set.
