# AGENTS.md

Guidance for AI coding agents working in the **pyBlink** repository.

## Project overview

pyBlink is a Python/Qt reimplementation of the PixInsight *Blink* tool for
reviewing astrophotography subframes, with extras for syncing images to/from
remote storage. Astronomers use it to blink through FITS frames, mark frames as
discarded/kept, detect star trails, and sync results with remote data sources
via `rclone`.

- **Language:** Python 3
- **GUI toolkit:** PySide6 (Qt for Python)
- **Entry point:** `pyBlink.py`

## Running the app

```sh
python3 -m venv .venv
. ./.venv/bin/activate
pip3 install -r requirements.txt
python3 pyBlink.py
```

## Key dependencies

`PySide6` (GUI), `astropy` (FITS I/O), `opencv-python` + `pillow` +
`auto-stretch` (image processing/stretching), `rclone-python` (remote sync,
requires the `rclone` binary installed), `platformdirs` (cache location),
`psutil` (username/process helpers).

## Architecture

| File | Role |
|------|------|
| `pyBlink.py` | `MainWindow`; wires up UI, image display, filtering radio buttons, and dialog actions. |
| `imageCache.py` | `imageCache` (QObject) — core model. Reads FITS headers/EXIF, stretches images, builds/persists the on-disk cache, emits Qt `Signal`s for progress. |
| `createCache.py` | Standalone/batch cache generation from a FITS directory (uses `imageCache._safe_username`). |
| `createCache.bat` | Windows helper that activates the venv and runs `createCache.py` (paths are machine-specific). |
| `syncDialog.py` | Remote sync (to/from server) progress dialog via `rclone`. |
| `localSyncDialog.py` | Local directory sync/import dialog. |
| `remoteProjectSyncDialog.py` | Browse/select remote projects; caches `rclone` lookups in a session-level classvar. |
| `deleteDialog.py` | Deletes discarded frames locally and remotely. |
| `config.json` | Runtime config: data sources, `rclone` cache/image paths, FITS aliases, last-used dir. Copy from `config.json.sample`. |

## UI files — IMPORTANT

- `*.ui` files are Qt Designer sources (edit these for layout changes).
- `ui_*.py` files are **generated** by `pyside6-uic` and must **not** be edited
  by hand — regenerate them instead:

  ```sh
  ./compileDesigns.sh
  ```

- `test.py` is a stray generated UI snapshot (not a real test suite); there is
  no automated test framework in this repo.

## Conventions

- Indentation is **2 spaces** (not the PEP 8 default of 4) — match the
  surrounding file.
- Cross-platform matters: Windows usernames are normalized via
  `_safe_username()` in `imageCache.py`; reuse it rather than calling
  `psutil` directly.
- Cache directory is resolved through `platformdirs.user_cache_dir`; don't
  hardcode paths.
- Keep/discard decisions are stored per user in `status-<username>.json`
  files next to the cache, so a frame's status is scoped to the reviewer.
  Only the current user's status file is written/synced (see `imageCache.py`,
  `syncDialog.py`, `localSyncDialog.py`).
- `config.json` is user/local state — don't commit machine-specific values;
  update `config.json.sample` when adding new config keys.

## Notes for agents

- There are no configured linters, formatters, or tests. Verify changes by
  running the app manually.
- After editing any `.ui` file, run `./compileDesigns.sh` and include the
  regenerated `ui_*.py`.
- Keep changes surgical; the code mixes model and Qt widget logic closely.
