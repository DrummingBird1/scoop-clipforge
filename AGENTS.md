# scoop-clipforge

Single source of truth for any AI agent working in this repository (Claude, Codex, Copilot, Cursor, Gemini, ChatGPT, Grok, OpenCode). `CLAUDE.md` only imports this file. Keep it self-contained: do not point to files outside the repository.

<!-- BEGIN core-rules v1 (generated from the shared core-rules.md; do not edit by hand) -->
## Core rules (apply to every agent)

- Read this file first. If `HANDOFF.local.md` exists next to it, read it too (local only, not in git).
- Never push, force-push or create remotes unless the owner explicitly asks. Work on a branch named `agent/<tool>-<topic>`; merge to `main` only through a pull request.
- Never commit or print secrets (`.env`, keys, tokens). Keep personal paths, emails and private repo names out of tracked files.
- Package managers: JavaScript uses `pnpm`, Python uses `uv`. Do not switch without being asked.
- Dev servers listen on `127.0.0.1` only, unless the owner asks otherwise.
- Do not delete or overwrite user data. Move it to an archive folder or ask first, and do a dry run before bulk changes.
- Make the smallest change that solves the task. Run this project's own check and test commands (see Run and Test in this file) and say what you ran and what you could not verify.
- If you have no access to the repository (a chat-only agent), return a unified diff or complete files, and list what the owner should verify.
<!-- END core-rules -->

## Purpose

A [Scoop](https://scoop.sh) bucket that installs ClipForge, a local video studio for Windows. The bucket holds one manifest, `bucket/clipforge.json`. Users install it with `scoop bucket add clipforge <this repository URL>` and `scoop install clipforge`.

## Type

- Package manifest repository, no application code and no build step. License terms are those of the packaged app (MIT, per the manifest).
- Files: `README.md` (user instructions) and `bucket/clipforge.json` (the Scoop manifest: `version`, `url`, `hash`, `extract_dir`, `shortcuts`, `persist`, `checkver`, `autoupdate`).
- The packaged app is a separate repository (`clipforge-app`). Each new version is published there as a GitHub Release with `ClipForge-<version>-win64.zip` and `SHA256SUMS.txt`.
- `persist` keeps `data` and `workspace` across updates. Do not remove them from the manifest: they hold the user's settings and videos.

## Run

- Install from a local manifest on a Windows machine with Scoop: `scoop install .\bucket\clipforge.json`.
- Update the manifest for a new release: set `version`, put the same version in `url` and `extract_dir`, and set `hash` to the zip's line in the Release's `SHA256SUMS.txt`. With Scoop installed, `checkver.ps1 -App clipforge -Dir bucket -Update` (in Scoop's `apps\scoop\current\bin`) does this from the manifest's `autoupdate` block.
- Not verified while writing this file: the commands above come from the packaged app's release notes in its repository, they were not run here.

## Test

- Keep `bucket/clipforge.json` valid JSON: `python -c "import json; json.load(open('bucket/clipforge.json'))"` (not verified here).
- Check a change end to end with `scoop install .\bucket\clipforge.json`, then `scoop uninstall clipforge` (without `--purge`, so user data is kept). Say what you ran and what you could not run.

## Rules

- The owner works in Hebrew: reply in Hebrew unless asked otherwise. Files and commit messages are in English.
- Never guess a hash. Copy the SHA-256 from the Release's `SHA256SUMS.txt` and compare it with the downloaded zip.
- Change only the manifest fields a release needs. Keep the `autoupdate` and `checkver` blocks working.
- One commit per released version, with the version in the subject.

## Do not

- Do not commit `.env`, keys, tokens or other secrets.
- Do not add large binaries (archives, video, audio, executables) to git; the zips stay on the app's GitHub Releases.
- Do not push or create a remote without the owner's explicit approval.

## State

- Public repository, default branch `main`. The manifest currently tracks the version shown in `bucket/clipforge.json`.

## Handoff

- Recent changes, unpushed work and open items are kept in `HANDOFF.local.md` next to this file. It is git-excluded and exists only on the owner's machine: read it when it is there, and do not copy its content into tracked files.
