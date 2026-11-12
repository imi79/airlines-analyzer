# 0024 · The app reloads its code when the hosting service updates it

Date: 2026-11-12 · Status: fix asked for by Imane ("fix this", with the hosting log), after the
M9 merge broke the public link

**What happened.** Streamlit Community Cloud follows `main`. When `main` changes, it pulls the
new files into the running app without restarting it. The entry file and the page files are
read again on every visit, but the modules they import stay in memory as they were. After the
M9 merge, the new Tearsheet page called `tearsheet.watch_checks(...)` on the copy of
`render/tearsheet.py` loaded before M9, which did not have it: every visit failed with
"module 'tearsheet.render.tearsheet' has no attribute 'watch_checks'". The tests and the
GitHub checks could not see it: they always start from a clean process.

Reproduced locally before fixing: the app started on the pre-M9 commit, the files switched to
`main` underneath it, the same error on the next visit.

**The fix.** At the top of `src/tearsheet/app/main.py`, before anything of the app is
imported, `fresh_code()` compares the app's source and config files (how many, and the latest
change time) with what was there when the code in memory was loaded. If they differ, it drops
the app's modules and Streamlit's caches, so everything is loaded again from the files. It
costs about a millisecond per visit and touches no figure.

**Checked.** The same local set-up, started on the fixed version and switched to a later
version that adds a function to a module and calls it from a page: the page shows the new
function's output, no error. A test covers the reload (`tests/test_app.py`).

**Limits.**

- The copy already running on the public link when this fix arrived had no record of what it
  loaded, so it could not heal itself: it needed one **reboot** (Streamlit Cloud, "Manage app",
  "Reboot app"). Every later update is covered.
- A change to the installed packages (`uv.lock`) is handled by the hosting service itself,
  which reinstalls and restarts.
- After each merge into `main`, open the public link once. A reboot remains the fallback for
  anything this guard does not foresee.
