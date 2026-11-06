#!/bin/sh
# The Ralph loop: run the agent on the same prompt, each time in a fresh session, until the
# goal check passes or the pass limit is reached.   Usage: sh ralph.sh [max passes, default 6]
max=${1:-6}
pass=1
while [ "$pass" -le "$max" ]; do
  if sh check.sh; then
    echo "Goal met after $((pass - 1)) passes."; exit 0
  fi
  echo "=== pass $pass of $max: $(date +%H:%M:%S) ==="
  opencode run --auto "$(cat PROMPT.md)" < /dev/null
  pass=$((pass + 1))
done
sh check.sh && echo "Goal met after $max passes." || echo "Stopped after $max passes; goal not met."
