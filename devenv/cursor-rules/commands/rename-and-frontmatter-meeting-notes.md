# Rename And Frontmatter Meeting Note

## Overview
Normalize a draft meeting note by renaming the file to the canonical `_Meetings/YYYY-MM-DD-title.md` pattern and refreshing the YAML frontmatter using prior company notes as references.

## Inputs
- `note_path`: Absolute path to the draft meeting note.
- `company_query`: Company or project keyword supplied by the user prompt (ask the user if missing).

## Preconditions
- The draft note lives in `_Meetings/`.
- `_Templates/Note-Meeting.md` defines the canonical structure.

## Steps
1. **Collect context**
   - Extract `company_query`, meeting date, title, and attendees from the prompt or note body; request missing pieces.
2. **Inspect the draft**
   - Load `note_path`; capture provisional frontmatter, headings, attendees, and tags.
   - Normalize the meeting date to ISO format with local timezone (e.g., `2025-09-30T09:00:00-07:00`).
3. **Reuse known metadata**
   - Search `_Meetings/` once for existing notes containing `company_query`.
   - Reuse recurring attendees, project, area, and tags when still relevant; merge with new attendees.
   - For each attendee candidate:
     - Check `_People/` once for a matching note; reuse the stored label if found.
     - If neither `_People/` nor past notes contain the person, stop searching and add a new entry formatted as `"[[Full Name COMPANY_NAME]]"` (uppercase company slug, preserve spacing in the name).
   - Ensure attendees use the quoted Obsidian backlink syntax.
4. **Rename the file**
   - Confirm the meeting title; slugify it (lowercase, kebab case, no special characters).
   - Prepend the meeting date (`YYYY-MM-DD`) to form the target filename.
   - Abort if a file with that name already exists.
   - Move the draft to `_Meetings/<new-file-name>.md`.
5. **Refresh frontmatter**
   - Start from `_Templates/Note-Meeting.md` frontmatter block.
   - Update fields per `meeting-notes-store.md` guidelines:
     - `type: meeting`
     - `date`: ISO timestamp
     - `attendees`: YAML list of quoted backlinks
     - `project`, `area`: single backlink values
     - `tags`: lowercase YAML list (no brackets)
     - `description`: concise summary if available
   - Keep `## Agenda`, `## Notes`, `## Actions` placeholders empty.
6. **Validate output**
   - Confirm final filename, frontmatter, and preserved note sections (transcript, agenda, notes, actions).
   - Report any remaining metadata requiring manual confirmation.

