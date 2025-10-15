# Store Meeting Notes (CLI Version)

## Overview
Create a meeting note in the vault by pulling metadata and transcripts from Granola via the CLI export command. This is Step 1 of a 2-step process:
1. **Export from Granola** (this command) - creates raw meeting note with transcript
2. **Normalize frontmatter** (use `/rename-and-frontmatter-meeting-notes`) - adds proper metadata, attendees, tags

## Inputs
- `query`: Text used to find the meeting via Granola CLI fuzzy search.
- `company_name` (optional): Company name to use when adding attendees (e.g., "Rivian", "Anyscale")

## Preconditions
- Meeting notes template exists at `_Templates/Note-Meeting.md` (note: hyphen, not em-dash)
- Granola CLI is installed and accessible via `uv run granola`

## Common Issues & Lessons Learned

⚠️ **Critical Issues to Avoid:**

1. **Truncated Meeting IDs**
   - ❌ BAD: `uv run granola export d16860f` (will fail with "Meeting not found")
   - ✅ GOOD: `uv run granola export d16860fe-bf58-4f01-8546-5d4fe00ecd20`
   - Always use the complete UUID from search results

2. **Missing --output-dir Flag**
   - ❌ BAD: `uv run granola export <id>` (will fail)
   - ✅ GOOD: `uv run granola export <id> --output-dir _Meetings`
   - The flag is REQUIRED despite CLI documentation suggesting it's optional

3. **HTML Tags Not Cleaned**
   - Raw exports contain `<h3>`, `<ul>`, `<li>`, `<hr>`, `&amp;` etc.
   - Must be converted to markdown automatically after export
   - Don't leave HTML in the final note

4. **Missing Frontmatter Enhancement**
   - Granola export only adds minimal frontmatter
   - Must run `/rename-and-frontmatter-meeting-notes` separately to add:
     - Proper attendees with [[Name COMPANY]] format
     - Tags from similar meetings
     - Description field
     - Project/area links

5. **Duplicate Content**
   - Granola sometimes exports both HTML version AND plain text version
   - Remove duplicates during HTML cleanup step

## Steps

### 1. Search and Select Meeting
**Option A: Fuzzy Search (Recommended)**
- Run `uv run granola search "<query>"` to find meetings using intelligent fuzzy matching
- The search supports multiple search types:
  - **Title search** (default): `uv run granola search "project planning"`
  - **Attendee search**: `uv run granola search "john" --attendees`
  - **Transcript search**: `uv run granola search "budget discussion" --transcript`
  - **Combined search**: `uv run granola search "meeting" --attendees --transcript`
- Parse the search results to extract meeting titles, dates, IDs, and match scores
- If multiple meetings match, present them as options for user selection
- Capture the selected `meeting_id` from the search results

**Option B: List All Meetings**
- Run `uv run granola list` to get all available meetings in a formatted table
- Parse the output to extract meeting titles, dates, and IDs
- If no meetings found, report that the Granola cache is empty or inaccessible
- If multiple meetings match the query, present them as options for user selection
- Capture the selected `meeting_id` from the table output

**Option C: Interactive Selection**
- Run `uv run granola export` without a meeting ID for an interactive selection menu
- User selects from the displayed list of meetings

### 2. Export Meeting to Markdown
- **IMPORTANT:** Use the COMPLETE meeting ID from search results (full UUID, not truncated)
- **REQUIRED:** Must specify `--output-dir _Meetings` (not optional despite CLI docs)
- Run `uv run granola export <full_meeting_id> --output-dir _Meetings`

The export command handles:
- ✅ Filename generation (date-prefixed, slugified title)
- ✅ Duplicate checking (won't overwrite existing files)
- ✅ Template loading from `_Templates/Note-Meeting.md`
- ⚠️ Frontmatter population (minimal - needs enhancement via `/rename-and-frontmatter-meeting-notes`)
- ✅ Transcript insertion with formatting
- ✅ File creation in `_Meetings/` directory

**Export Command:**
```bash
# Standard export (REQUIRED format)
uv run granola export <full_meeting_id> --output-dir _Meetings

# Example with full UUID
uv run granola export d16860fe-bf58-4f01-8546-5d4fe00ecd20 --output-dir _Meetings
```

**⚠️ Common Export Issues:**
- Meeting ID must be complete UUID (e.g., `d16860fe-bf58-4f01-8546-5d4fe00ecd20`)
- Truncated IDs like `d16860f` will fail with "Meeting not found"
- The `--output-dir` flag is REQUIRED (CLI will fail without it)

### 3. Clean Up HTML Formatting
After export, the notes section will contain HTML tags that need conversion to markdown:
- Convert `<h3>` → `###` headers
- Convert `<ul><li>` → bullet lists (`-`)
- Convert `<ol><li>` → numbered lists
- Convert `<hr>` → `---`
- Convert `<p>` and `<a>` → clean markdown
- Replace `&amp;` → `&`
- Remove duplicate content (Granola sometimes exports both HTML and plain text versions)

**AI should automatically:**
1. Detect HTML tags in the notes section
2. Convert all HTML to clean markdown
3. Remove any duplicate content sections

### 4. Prompt for Frontmatter Normalization
After successfully exporting and cleaning HTML, ask the user:
> "Would you like to normalize the frontmatter and add attendees/tags? (This will run `/rename-and-frontmatter-meeting-notes`)"

If yes, automatically trigger the frontmatter normalization command.

### 5. Verify and Report
- Check the CLI output for the created file path
- Report the file location and summary to the user
- If the file already exists, the CLI will warn and not overwrite
- List any HTML tags that were converted to markdown
- Remind user about frontmatter normalization if not done yet

## CLI Commands Reference

### Export Meeting (Primary Command)
```bash
# REQUIRED format - must specify --output-dir
uv run granola export <full_meeting_id> --output-dir _Meetings

# Example with complete UUID
uv run granola export d16860fe-bf58-4f01-8546-5d4fe00ecd20 --output-dir _Meetings

# Interactive selection (if you don't have meeting ID)
# Note: This may not work reliably - prefer search + export with ID
uv run granola export
```

**Export Features:**
- **Automatic Filename**: Generates `YYYY-MM-DD-slugified-title.md` format
- **Duplicate Prevention**: Won't overwrite existing files
- **Template Processing**: Fills minimal frontmatter (needs enhancement)
- **Transcript Formatting**: Preserves speaker labels and timestamps
- ⚠️ **HTML in Notes**: Exports HTML tags that need markdown conversion
- ⚠️ **Duplicate Content**: Sometimes exports both HTML and plain text versions

### Search Meetings (Fuzzy Matching)
```bash
# Basic title search (default behavior)
uv run granola search "project planning"

# Search participant names
uv run granola search "john" --attendees

# Search transcript content (slower but comprehensive)
uv run granola search "budget discussion" --transcript

# Combine search types
uv run granola search "meeting" --attendees --transcript

# JSON output for programmatic use
uv run granola search "quarterly review" --json
```

**Search Features:**
- **Fuzzy Matching**: Uses intelligent fuzzy matching (60%+ threshold) with confidence scores
- **Multiple Fields**: Search titles, attendees, or transcript content
- **Smart Filtering**: By default excludes meetings with no transcript content
- **Flexible Output**: Table (default), JSON, or YAML formats
- **Match Scoring**: Shows what matched and confidence score (e.g., "Title (95%)")

### List Meetings
```bash
uv run granola list
```
- Shows formatted table with title, date, duration, platform, transcript stats, participants, and ID
- Use `--show-ignored` to see ignored meetings

### Get Meeting Details (For Manual Review)
```bash
uv run granola get [meeting_id]
```
- Returns comprehensive markdown with metadata, transcript, and documents
- Use `--clipboard` to copy output to clipboard
- Use `--output file.md` to save to file
- **Note**: For creating notes, use `export` command instead

## Search Output Formats

### Table Output (Default)
```
                           Search Results for 'project planning'                           
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Title                                     ┃ Date     ┃ Dur ┃ Platform ┃ Transcr… ┃ Ppl ┃ Match     ┃ ID       ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━┩
│ Q4 Planning Meeting                       │ 10/09    │ 60m │ Zoom     │ 2.5k     │ 5   │ Tit (95%) │ abc123…  │
│ Project Kickoff Discussion               │ 10/08    │ 45m │ Teams    │ 1.8k     │ 3   │ Tit (87%) │ def456…  │
└───────────────────────────────────────────┴──────────┴─────┴──────────┴──────────┴─────┴───────────┴──────────┘
```

### JSON Output
```json
{
  "query": "project planning",
  "total_results": 2,
  "meetings": [
    {
      "id": "abc123...",
      "title": "Q4 Planning Meeting",
      "date": "2025-10-09 14:30",
      "duration_minutes": 60,
      "platform": "Zoom",
      "participants": ["john", "sarah", "mike"],
      "participant_count": 3,
      "transcript_stats": "2,500 words",
      "match": {
        "type": "Title",
        "score": 95
      }
    }
  ],
  "search_options": {
    "attendees": false,
    "transcript": false,
    "show_ignored": false,
    "include_empty_transcripts": false
  }
}
```

### YAML Output
```yaml
query: project planning
total_results: 2
meetings:
- id: abc123...
  title: Q4 Planning Meeting
  date: 2025-10-09 14:30
  duration_minutes: 60
  platform: Zoom
  participants:
  - john
  - sarah
  - mike
  participant_count: 3
  transcript_stats: 2,500 words
  match:
    type: Title
    score: 95
search_options:
  attendees: false
  transcript: false
  show_ignored: false
  include_empty_transcripts: false
```

## Error Handling
- **Export Errors**:
  - If file already exists: CLI will abort and warn about duplicate
  - If template not found: Specify custom template with `--template` flag
  - If meeting ID invalid: Re-run search to get current IDs
  - If transcript is empty: CLI will still create the note with available metadata

- **Search Errors**:
  - If no results found: Try broader search terms or use `--include-empty-transcripts`
  - If CLI fails: Check Granola installation and cache file at `~/Library/Application Support/Granola/cache-v3.json`
  - For slow searches: Transcript search is slower for large datasets

- **Common Issues**:
  - Missing cache file: Verify Granola has processed recent meetings
  - Permission errors: Check write permissions for output directory
  - Template errors: Ensure `_Templates/Note—Meeting.md` exists and is valid

## Search Examples

### Finding Meetings by Topic
```bash
# Find planning meetings
uv run granola search "planning" --transcript

# Find architecture discussions
uv run granola search "architecture" --attendees --transcript

# Find budget-related meetings
uv run granola search "budget" --transcript --json
```

### Finding Meetings by People
```bash
# Find meetings with specific people
uv run granola search "john" --attendees
uv run granola search "sarah" --attendees --yaml

# Find meetings with team leads
uv run granola search "team lead" --attendees --transcript
```

### Finding Meetings by Content
```bash
# Find meetings discussing specific topics
uv run granola search "deadline" --transcript
uv run granola search "technical debt" --transcript --include-empty-transcripts

# Find meetings with specific outcomes
uv run granola search "decision" --transcript --json
```

## Workflow Summary

### Recommended Workflow (2 cursor commands)
```
# Step 1: Export and clean (this command)
/meeting-notes-store Rivian Technical Workshop

# Step 2: Add frontmatter (separate command) 
/rename-and-frontmatter-meeting-notes @2025-10-10-rivian-technical-workshop.md Rivian
```

### Manual CLI Workflow (for reference)
```bash
# 1. Search for meeting
uv run granola search "Rivian Technical Workshop" --json

# 2. Export with FULL UUID
uv run granola export d16860fe-bf58-4f01-8546-5d4fe00ecd20 --output-dir _Meetings

# 3. Manually clean HTML → markdown (AI does this automatically)
# 4. Manually add frontmatter (use cursor command instead)
```

## AI Behavior

**Step-by-Step Workflow:**

1. **Search for Meeting**
   - Use `uv run granola search "<query>" --json` for programmatic parsing
   - Extract the COMPLETE meeting ID (full UUID) from results
   - If multiple results, present options to user with title, date, transcript size
   - Never use truncated meeting IDs

2. **Export Meeting**
   - Run `uv run granola export <full_meeting_id> --output-dir _Meetings`
   - Verify the export succeeded and capture the output file path
   - If export fails with "Meeting not found", check if ID is complete UUID

3. **Automatically Clean HTML** (REQUIRED)
   - Read the exported file
   - Detect HTML tags in the `## Notes` section
   - Convert ALL HTML to clean markdown:
     - `<h3>` → `###`
     - `<ul><li>` → `-` bullet lists with proper indentation
     - `<ol><li>` → `1.`, `2.`, `3.` numbered lists
     - `<hr>` → `---`
     - `<p><a href="">` → `[text](url)`
     - `&amp;` → `&`
     - `&lt;` → `<`, `&gt;` → `>`
   - Remove duplicate content sections (if HTML and plain text both exist)
   - Preserve the transcript section as-is

4. **Prompt for Frontmatter Enhancement**
   - After HTML cleanup, ask: "Would you like to add proper frontmatter with attendees and tags?"
   - If yes, note the company name from context and inform user they should run:
     `/rename-and-frontmatter-meeting-notes @<filename> <company_name>`
   - If company name is ambiguous, ask user to specify

5. **Report Results**
   - ✅ File path created
   - 📊 Meeting summary (title, date, transcript word count)
   - 🔧 HTML tags converted (list what was cleaned)
   - 📝 Next step reminder about frontmatter normalization

**Do:**
- Always use COMPLETE meeting ID (full UUID)
- Always specify `--output-dir _Meetings`
- Always clean up HTML tags automatically
- Always prompt about frontmatter normalization
- Use JSON output for search (`--json`) for reliable parsing
- Present multiple search results as clear options

**Don't:**
- Use truncated meeting IDs (e.g., `d16860f` instead of full UUID)
- Skip the HTML cleanup step
- Leave HTML tags in the notes
- Manually generate filenames (CLI does this)
- Try to add attendees or tags in this step (that's Step 2)
- Forget to prompt about frontmatter normalization

## Output
When the command completes successfully, report to the user:
- ✅ **File created:** `_Meetings/YYYY-MM-DD-meeting-title.md`
- 📊 **Meeting summary:** Title, date, transcript word count
- 🔍 **Search match:** Match type and confidence score (if search was used)
- 🔧 **HTML cleaned:** List of conversions made (e.g., "Converted 3 `<h3>` headers, 5 `<ul>` lists to markdown")
- 📝 **Next step:** Prompt about running `/rename-and-frontmatter-meeting-notes` to add attendees/tags
- ⚠️ **Warnings:** Any issues from the CLI (missing transcript, metadata issues, etc.)

## Complete Two-Step Workflow

This command is Step 1 of 2. Here's the complete workflow:

### Step 1: Export & Clean (this command)
```
User runs: /meeting-notes-store Rivian Technical Workshop

AI does:
1. Search: uv run granola search "Rivian Technical Workshop" --json
2. Export: uv run granola export <full_uuid> --output-dir _Meetings
3. Clean HTML: Convert all <h3>, <ul>, <li>, etc. to markdown
4. Prompt: "Add frontmatter with attendees/tags?"
```

**Result:** Clean markdown file with transcript, but minimal frontmatter

### Step 2: Normalize Frontmatter (separate command)
```
User runs: /rename-and-frontmatter-meeting-notes @<filename> Rivian

AI does:
1. Search existing meetings for similar company/attendees
2. Add proper attendees as [[Name COMPANY]] backlinks
3. Add tags based on similar meetings
4. Rename file if title needs improvement
5. Add description field
```

**Result:** Fully formatted meeting note with proper metadata, attendees, tags, and clean markdown