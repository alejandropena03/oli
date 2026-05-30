# HOW TO USE THE OLI DOCS

Put `OLI_MASTER_SPEC.md` inside the repo at:

`docs/OLI_MASTER_SPEC.md`

Then paste `CLAUDE_CODE_START_PROMPT.md` into Claude Code.

The master spec is the product constitution. It tells Claude what Oli is, what it is not, how missions work, how memory works, how trust works, what to build first, and what not to fake.

The start prompt is the first build instruction. It forces Claude to start with the Mission Kernel instead of jumping into pretty UI.

Recommended first repo flow:

1. Create a new repo called `oli`.
2. Add `docs/OLI_MASTER_SPEC.md`.
3. Paste `CLAUDE_CODE_START_PROMPT.md` into Claude Code.
4. Let Claude propose a stack and structure.
5. Approve only if the proposal preserves the Mission Kernel, memory, evidence, permissions, and modular architecture.
6. Build V0.
7. Use V0 to generate the next spec for V1.

Do not treat V0 as a launch product. V0 is the foundation.
