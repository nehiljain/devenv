# Update Latest Anyscale Docs

## Overview
Refresh the local Anyscale documentation snapshot in `anyscale-context-kit` and mirror it into the vault inbox.

## Steps
1. **Capture current counts**
   - `PREV_COUNT=$(find /Users/nehil/code/obsidian-vault/00-Inbox/anyscale-docs -type f 2>/dev/null | wc -l | tr -d ' ')`
2. **Fetch the latest docs**
   - `cd /Users/nehil/code/anyscale-context-kit`
   - `uv run fetch-anyscale-docs`
3. **Replace the inbox copy**
   - `rm -rf /Users/nehil/code/obsidian-vault/00-Inbox/anyscale-docs`
   - `cp -R /Users/nehil/code/anyscale-context-kit/anyscale-docs /Users/nehil/code/obsidian-vault/00-Inbox/`
4. **Spot-check**
   - `ls /Users/nehil/code/obsidian-vault/00-Inbox/anyscale-docs | head`
5. **Verify file count**
   - `SRC_COUNT=$(find /Users/nehil/code/anyscale-context-kit/anyscale-docs -type f | wc -l | tr -d ' ')`
   - `DEST_COUNT=$(find /Users/nehil/code/obsidian-vault/00-Inbox/anyscale-docs -type f | wc -l | tr -d ' ')`
   - `if [ $((SRC_COUNT > DEST_COUNT ? SRC_COUNT - DEST_COUNT : DEST_COUNT - SRC_COUNT)) -gt 10 ]; then echo "Warning: source and inbox differ: $SRC_COUNT vs $DEST_COUNT"; fi`
   - `if [ -n "$PREV_COUNT" ] && [ $((DEST_COUNT > PREV_COUNT ? DEST_COUNT - PREV_COUNT : PREV_COUNT - DEST_COUNT)) -gt 10 ]; then echo "Warning: inbox changed from $PREV_COUNT to $DEST_COUNT"; fi`

