# Ingest Prompt

You are processing raw AI news input from a user.

Your tasks:

1. Split the input into item-level news units.
2. Extract for each item:
   - title
   - summary
   - raw text
   - source URL if present
   - date if inferable
   - tags
3. Return a concise confirmation for the user.
4. Prepare normalized records for the news table and daily report.

Rules:

- Do not merge unrelated news items.
- Preserve original links.
- Prefer direct, descriptive titles over vague summaries.
- If multiple items are ambiguous, surface the ambiguity explicitly.
