# Roadmap: scoop-clipforge

A [Scoop](https://scoop.sh) bucket that installs [ClipForge](https://github.com/DrummingBird1/clipforge-app), a local video studio for Windows. The bucket holds one manifest, `bucket/clipforge.json`.

This file is the source of truth for the project plan. There is no separate changelog: the git log has one commit per released version.

## Current state

- Stage: released. The manifest tracks ClipForge 2.0.1 (commit "ClipForge 2.0.1", 2026-11-17).
- History so far: 1.1.2 and 1.1.3 (2026-10-30), 1.2.0 (2026-11-08), 2.0.1 (2026-11-17).
- The manifest covers install, Start menu shortcut, `persist` for `data` and `workspace`, `checkver` and `autoupdate` (version, URL and SHA-256 come from the app's GitHub Release).
- Docs: `README.md` (user instructions) and `AGENTS.md` (agent guide).
- Project tracker: no Trello board was created; the workspace is at its open-board limit.

## Routine work

- On each new ClipForge release: update `version`, `url`, `hash` and `extract_dir` in `bucket/clipforge.json`, taking the hash from the release's `SHA256SUMS.txt`. One commit per version.
- Keep `persist` (`data`, `workspace`) and the `checkver` and `autoupdate` blocks working.

## Open questions

- An end-to-end install and update with Scoop (`scoop install .\bucket\clipforge.json`, `scoop update clipforge`) is not documented as verified for any release. Is there a machine with Scoop to run it on?
- The attestation of the release zip has not been checked. Is that wanted as part of each release?
- Should the manifest's `autoupdate` be relied on (Scoop's own bucket automation) instead of manual version commits?

No further plan is recorded; nothing is planned beyond following ClipForge releases.
