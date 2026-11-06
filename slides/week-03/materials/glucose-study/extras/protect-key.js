// Copy to .opencode/plugins/protect-key.js, then restart OpenCode.
// Runs before every tool call (read, grep, bash, ...). If the call's arguments mention
// the protected name, the call is stopped and the agent sees the error message.
const PROTECTED = "linkage-key"

export const ProtectKey = async () => ({
  "tool.execute.before": async (input, output) => {
    const args = JSON.stringify(output.args ?? {})
    if (args.includes(PROTECTED)) {
      throw new Error(
        `Blocked by protect-key.js: ${PROTECTED} must not be read by the agent. ` +
        "Stop and ask the user."
      )
    }
  },
})
