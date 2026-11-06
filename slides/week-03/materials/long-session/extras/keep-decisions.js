// Copy to .opencode/plugins/keep-decisions.js, then restart OpenCode.
// Runs when a session is compacted. Adds DECISIONS.md to what the summary must keep.
import { readFile } from "node:fs/promises"

export const KeepDecisions = async ({ directory }) => ({
  "experimental.session.compacting": async (input, output) => {
    const text = await readFile(`${directory}/DECISIONS.md`, "utf8").catch(() => "")
    if (text) {
      output.context.push(
        "Rules and decisions from DECISIONS.md. Copy them into the summary word for word:\n\n" + text
      )
    }
  },
})
