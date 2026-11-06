#!/bin/sh
# The goal, as a command: exit 0 only when every test passes, none is skipped, and the tests,
# pytest.ini and this file are as they were at the tag `start`. The agent's own claim that it
# is done does not count.
guarded="tests pytest.ini check.sh"
if [ -n "$(git status --porcelain -- $guarded)" ] || ! git diff --quiet start -- $guarded; then
  echo "FAIL: tests/, pytest.ini or check.sh was changed"; exit 1
fi
# --noconftest: a conftest.py added anywhere cannot skip or rewrite the tests.
if ! python3 -m pytest -q --noconftest tests > .last-check.txt 2>&1; then
  echo "not yet: $(tail -n 1 .last-check.txt)"; exit 1
fi
if grep -qE "skipped|xfail|xpass" .last-check.txt; then
  echo "FAIL: $(tail -n 1 .last-check.txt)"; exit 1
fi
echo "PASS: $(tail -n 1 .last-check.txt), tests unchanged"
