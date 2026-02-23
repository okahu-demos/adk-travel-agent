---
name: monocle
description: Analyze Monocle trace JSON files. Use for debugging agent test failures, answering questions about traces, or inspecting agent behavior.
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
argument-hint: "[optional: question or specific error/test name to focus on]"
---

# Monocle Agent Test Analyzer

You analyze ADK (Agent Development Kit) agent traces using Monocle observability data.

## Determine the Mode

Based on the user's message, determine which mode to operate in:

- **Query mode**: The user is asking a question about traces (e.g., "what is the latest run about?", "any issues?", "show me the agent flow"). In this mode, **do NOT archive or move any files**. Just read and answer.
- **Debug mode**: The user wants to fix a test failure or apply code changes (e.g., "fix this", "debug the failure", "why did the test fail and fix it"). In this mode, follow the full debug workflow including archiving.

If unclear, default to **query mode** (read-only, no archiving).

---

## Query Mode (read-only)

### Step 1: Find Traces

Search for trace files in both `.monocle/` and `.monocle_archive/`. Use Glob to find files matching `.monocle/**/*.json` and `.monocle_archive/**/*.json`. Prefer the most recent files (by filename timestamp or modification time).

If no JSON files are found anywhere, inform the user and stop.

### Step 2: Read and Analyze

Read the relevant trace JSON file(s). Extract and present information based on the user's question. Key fields:

- **Test status**: `"test.status"` field (`"passed"` or `"failed"`)
- **Assertion messages**: `"test.assertion.message"` for failure reasons
- **Agent flow**: Reconstruct execution chain via `parent_id` relationships
- **Agent names**: `"entity.1.name"` fields
- **Tool invocations**: Spans with `"span.type": "agentic.tool.invocation"`
- **LLM inputs/outputs**: `events` arrays with `data.input` and `data.output`
- **Model used**: `"entity.2.name"`
- **Span types**: `workflow` -> `agentic.turn` -> `agentic.invocation` -> `inference` / `agentic.tool.invocation`

Answer the user's question concisely. Note any observations (e.g., tools not called, unexpected responses) even if the test passed.

---

## Debug Mode (read-write with archiving)

### Step 1: Archive Stale Traces, Then Find the Latest

Archive any existing JSON files in `.monocle/` from prior runs so analysis starts clean. Use the archive bash snippet (see below). If there are no files to archive, skip silently.

Then run the failing test (if the user hasn't already), which will generate fresh traces.

Search `.monocle/` recursively for all JSON files using Glob matching `.monocle/**/*.json`.

If no JSON files are found in `.monocle/`, inform the user and stop.

### Step 2: Read and Analyze the Traces

Read the latest Monocle trace JSON file(s). Focus on extracting:

- **Test status**: Look for `"test.status"` field (`"passed"` or `"failed"`) in span attributes
- **Assertion messages**: Look for `"test.assertion.message"` field for the exact failure reason
- **Agent flow**: Reconstruct the agent execution chain by following `parent_id` relationships between spans
- **Agent names**: Extract from `"entity.1.name"` fields (e.g., `adk_flight_booking_agent`, `adk_hotel_booking_agent`)
- **Tool invocations**: Look for spans with `"span.type": "agentic.tool.invocation"` to see which tools were called
- **LLM inputs/outputs**: Check `events` arrays for `data.input` and `data.output` events to understand what each agent received and responded
- **Model used**: Check `"entity.2.name"` for the model (e.g., `gemini-2.5-flash`)
- **Span types**: `workflow` -> `agentic.turn` -> `agentic.invocation` -> `inference` / `agentic.tool.invocation`

### Step 3: Diagnose the Issue

Based on the trace analysis, determine:

1. **Which test failed** and what the assertion expected vs what happened
2. **Which agent(s)** behaved incorrectly in the execution chain
3. **Whether a tool was expected but not called** (common: `"Tool 'X' was not invoked"`)
4. **Whether the LLM response was off** — check if the agent's system prompt is missing context, or if the model chose not to call a tool when it should have
5. **Whether the agent configuration is wrong** — missing tools, wrong instructions, incorrect sub-agent wiring

Compare failed traces against any passing traces (if available in the same batch) to pinpoint what differs.

### Step 4: Read the Relevant Source Code

Based on the diagnosis, read the relevant source files:

- Agent definitions (look for `LlmAgent`, `SequentialAgent` configurations)
- Tool function definitions (the functions passed to agent `tools=[]`)
- Test files in `tests/` to understand what the test expects
- Any config/setup files
- DO NOT fix the test itself or any file in ./tests folder. If you suspect it is flaky test, out the findings

### Step 5: Propose and Apply the Fix

Based on the trace analysis and source code review:

1. Explain the root cause clearly to the user
2. Show the trace evidence (quote relevant input/output/assertion from the JSON)
3. Propose a specific code fix
4. Apply the fix using Edit/Write tools

Common fixes include:
- Updating agent `instruction` prompts to be more directive about tool usage
- Adding missing tools to an agent's `tools=[]` list
- Fixing tool function signatures or return values
- Adjusting agent descriptions for proper routing

### Step 6: Archive Monocle Traces

After analysis is complete (and after any verification test re-runs), archive ALL JSON files from `.monocle/` to `.monocle_archive/`.

**IMPORTANT:** Only archive in debug mode, never in query mode.

Use this bash snippet for archiving:

```bash
# Create archive dir, move files with timestamp prefix, preserve structure
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
find .monocle -name "*.json" -type f | while read f; do
  REL="${f#.monocle/}"
  DIR=".monocle_archive/$(dirname "$REL")"
  mkdir -p "$DIR"
  BASENAME=$(basename "$REL")
  mv "$f" "$DIR/${TIMESTAMP}_${BASENAME}"
done
```

---

## Additional Context

$ARGUMENTS
