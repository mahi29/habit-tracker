# Bedside Habit Tracker

A dead-simple, single-file habit tracker meant to live on an always-on tablet by your bed. Tap a big box when you do a habit; the boxes reset every day; history is kept so you can see a month-at-a-glance grid like a paper flashcard.

- **One file, no build, no backend.** Everything is in `index.html`.
- **Data stays on the device** (browser `localStorage`). Use Export/Import in Settings to back it up.
- **Dark theme**, large tap targets, 2-column tile grid.
- **Always-on friendly:** auto-dims at night, tap to wake, gentle pixel-shift to avoid OLED burn-in, and a screen wake lock so the tablet won't sleep.

## Run it locally

Just open the file — no server needed:

```
open index.html        # macOS
```

Or double-click `index.html` in a file browser.

## Use it

- **Today screen:** tap a tile to mark a habit done (fills green with a ✓); tap again to undo. The counter at top shows `done/total`.
- **History (calendar icon):** the flashcard grid — one row per habit, one column per day of the month, with monthly totals. Use ‹ › to scroll through past months.
- **Settings (gear icon):**
  - Add a habit (type a name, tap **+**).
  - Rename (tap the name), reorder (▲▼), or remove (🗑). Removing a habit hides it from today but **keeps its past history**.
  - Set the **night dimming** hours.
  - **Export** downloads a `habits-backup-YYYY-MM-DD.json` file. **Import** restores from one.

Habits reset automatically at local midnight — including while the page stays open.

## Deploy so the tablet can always load it

Any static host works since it's a single file. Two easy free options:

### GitHub Pages
1. Create a repo and add `index.html` at the root.
2. Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch**, pick `main` / `/root`, save.
3. Your URL will be `https://<you>.github.io/<repo>/`.

### Vercel / Netlify
1. Drag-and-drop the folder onto [vercel.com](https://vercel.com/new) or [app.netlify.com/drop](https://app.netlify.com/drop), or connect the repo.
2. No build command, no framework — it deploys the static file as-is.

## Put it on the tablet

1. Open the deployed URL in the tablet's browser.
2. **Add to Home Screen** (Share menu on iPad / browser menu on Android) for a full-screen, app-like icon.
3. Plug the tablet in and set the display to stay on (e.g. iPad: Settings → Display → Auto-Lock → Never; or use Guided Access to lock it to the app). The app also requests a wake lock to help keep the screen on.

## Backups

Because data lives only in the tablet's browser, **export occasionally** (Settings → Export) and keep the JSON somewhere safe. Clearing the browser's site data or switching tablets will otherwise lose history. Import the file on a new device to restore everything.

## Notes / future ideas

- A motivational-quote slot is already wired in (the message that appears when all habits are done) — easy to expand later into a rotating quote list.
- Data shape (in `localStorage` under `habitTracker:v1`):
  ```json
  {
    "habits":  [ { "id": "h1", "name": "Workout", "order": 0, "archived": false } ],
    "log":     { "2026-06-23": ["h1","h3"] },
    "settings": { "nightDimStartHour": 21, "nightDimEndHour": 7 }
  }
  ```
