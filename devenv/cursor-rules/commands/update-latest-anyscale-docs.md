# Update Latest Anyscale Docs

## Overview
Build/update Anyscale documentation context for LLM-assisted development using the globally-installed `asck` tool.

## Prerequisites
Ensure `asck` is installed globally via devenv:
```bash
devenv tools install --tool asck
```

## Usage

### Build Context in Current Directory
```bash
# Creates ./anyscale-docs/ with latest documentation
asck build-context
```

### Build Context in Specific Location
```bash
# Creates documentation at specified path
asck build-context --output-dir /workspace/docs/anyscale
```

### Update Existing Context
```bash
# Refreshes documentation in existing directory
cd /path/to/your/project
asck build-context --force  # Force rebuild to get latest
```

## What It Does
- Downloads complete Anyscale documentation library
- Includes curated best practices and optimizations
- Creates unified context ready for AI assistants

## Tell Your AI Assistant
After building:
```
"I've built the Anyscale context at ./anyscale-docs. 
Use them as reference when helping me build my Ray application."
```

## Verify Installation
```bash
# Check if asck is installed
asck --help

# If not installed
devenv tools install --tool asck
```

