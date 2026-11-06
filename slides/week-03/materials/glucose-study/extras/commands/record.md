---
description: Append a reproducibility record of the current task to RECORD.md
---
Append an entry to RECORD.md (create it if it does not exist) for this task: $ARGUMENTS

The entry has: the date (!`date +%F`); the model you are running as; what was asked, in one
or two sentences; the files that changed:

!`git status --short`

!`git diff --stat`

and how the result was checked: the commands and the numbers they printed. List only
checks that were actually run in this session. If nothing was checked, write "not checked".
