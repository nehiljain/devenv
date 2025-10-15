# Stop orphan notes now

## Overview
Sweep the vault root for orphan notes using plain shell commands, send each to its canonical folder, and fold stray clippings into the inbox.

## Steps
1. **Run from the vault root**
   - `cd /Users/nehil/code/obsidian-vault`
2. **See the current layout**
   - `tree -L 2`
3. **Preview every loose markdown file**
   - `for f in *.md; do
       if [ "$f" = 'Home.md' ] || [ "$f" = 'Start Here.md' ]; then
         continue
       fi
       echo "=== $f ==="
       sed -n '1,20p' "$f"
       echo
     done`
4. **Move orphan notes based on their `type`**
   - `for f in *.md; do
       case "$f" in
         'Home.md'|'Start Here.md')
           continue
           ;;
       esac
       note_type=$(awk -F': *' 'tolower($1)=="type" {print tolower($2); exit}' "$f")
       case "$note_type" in
         meeting) dest="_Meetings" ;;
         person) dest="_People" ;;
         project) dest="10-Projects" ;;
         area) dest="20-Areas" ;;
         resource) dest="30-Resources" ;;
         *) echo "SKIP $f (no type match)" && continue ;;
       esac
       if [ -e "$dest/$f" ]; then
         echo "SKIP $f (already exists in $dest)"
       else
         mv "$f" "$dest/" && echo "MOVED $f -> $dest/"
       fi
     done`
5. **Relocate stray clippings into the inbox**
   - `if [ -d Clippings ]; then
       mkdir -p '00-Inbox/Clippings'
       for item in Clippings/*; do
         [ -e "$item" ] || continue
         base=$(basename "$item")
         if [ -e "00-Inbox/Clippings/$base" ]; then
           echo "SKIP $base (already inside inbox)"
         else
           mv "$item" "00-Inbox/Clippings/" && echo "MOVED $base -> 00-Inbox/Clippings/"
         fi
       done
       rmdir Clippings 2>/dev/null && echo 'REMOVED empty Clippings directory'
     else
       echo 'No stray Clippings directory at vault root'
     fi`
6. **Purge temporary scratch directories**
   - `for dir in tmp tmp-whisper-test; do
       if [ -d "$dir" ]; then
         rm -rf "$dir" && echo "REMOVED $dir"
       else
         echo "$dir already absent"
       fi
     done`
7. **Confirm the vault root only holds expected notes**
   - `ls -1 *.md`

## Notes
- Add a `type` field to each template so the move loop can find the right folder.
- Extend the `case` block if you introduce new canonical folders.

