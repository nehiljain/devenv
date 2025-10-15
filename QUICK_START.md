# DevEnv Quick Start

## One-Line Install

```bash
uv pip install git+https://github.com/nehiljain/devenv.git
```

## Commands

```bash
# Setup cursor rules in current project
devenv setup

# Force setup (backup existing .cursor)
devenv setup --force

# Check status
devenv status

# Get info about installation
devenv info

# Diagnose issues
devenv doctor

# Remove symlink
devenv unlink

# List available global tools
devenv tools list

# Install all global tools
devenv tools install

# Install specific tool
devenv tools install --tool asck

# Check which tools are installed
devenv tools check
```

## Typical Workflow

### First Time Setup
```bash
# Clone devenv for editing rules
git clone https://github.com/nehiljain/devenv.git ~/devenv

# Install in a project
cd ~/projects/my-project
uv pip install git+https://github.com/nehiljain/devenv.git
devenv setup
```

### Update Rules
```bash
# Edit rules
cd ~/devenv/devenv/cursor-rules
vim rules/writing/my-rule.mdc

# Push changes
cd ~/devenv
git add .
git commit -m "Update rules"
git push

# On other machines
cd ~/devenv && git pull
# All symlinked projects see updates immediately
```

### Remote Workspace
```bash
ssh remote-host
uv pip install git+https://github.com/nehiljain/devenv.git
cd /workspace
devenv setup
devenv tools install  # Install global tools like asck
```

### Install Global Tools
```bash
# List available tools
devenv tools list

# Install all configured tools (asck, etc.)
devenv tools install

# Check what's installed
devenv tools check
```

## What It Does

Creates a symlink:
```
your-project/.cursor → /path/to/installed/devenv/cursor-rules
```

All Cursor commands and rules are centralized. Edit once, update everywhere.

## Troubleshooting

```bash
# Check if properly linked
devenv status

# Diagnose issues
devenv doctor

# Force reinstall
uv pip uninstall devenv
uv pip install git+https://github.com/nehiljain/devenv.git
devenv setup --force
```

## Repository

https://github.com/nehiljain/devenv

