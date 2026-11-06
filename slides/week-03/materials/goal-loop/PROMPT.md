You are one pass of a loop. You remember nothing from earlier passes: PLAN.md, NOTES.md
and `git log` are the memory.

1. Read PLAN.md and NOTES.md.
2. Take the first item in PLAN.md that is not ticked. Work on that item only.
3. Implement it in glucose_tools.py. Never change anything in tests/.
4. Run `python3 -m pytest -q tests`. This item's tests must pass, and the tests of the items
   already ticked must still pass.
5. Tick the item in PLAN.md, add one line to NOTES.md (what you did, and anything the next
   pass should know), then `git add -A && git commit -m "item N: <short title>"`.
6. Stop. Do not start the next item.

If you are stuck, write why in NOTES.md, commit, and stop.
