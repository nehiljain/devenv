# DevEnv - Personal Development Environment Setup

Manage Cursor rules and configuration across all your projects with a single command.

## What It Does

DevEnv centralizes your Cursor rules and commands in one place, then symlinks them to any project you want. When you update rules in the central location, all linked projects automatically see the changes.

## Installation

Install directly from GitHub:

```bash
uv pip install git+https://github.com/nehiljain/devenv.git
```

Or clone and install locally:

```bash
git clone https://github.com/nehiljain/devenv.git
cd devenv
uv pip install -e .
```

## Quick Start

Setup Cursor rules in your current project:

```bash
cd ~/projects/my-project
devenv setup
```

That's it! Your project now has a `.cursor` directory symlinked to the central rules.

## Commands

### `devenv setup`

Create symlinks for Cursor rules in a project directory.

```bash
# Setup in current directory
devenv setup

# Setup in specific directory
devenv setup --target-dir ~/projects/my-project

# Force setup (backup existing .cursor if present)
devenv setup --force
```

### `devenv status`

Check if Cursor rules are properly linked.

```bash
devenv status

# Check specific directory
devenv status --target-dir ~/projects/my-project
```

### `devenv info`

Display devenv installation information.

```bash
devenv info
```

### `devenv doctor`

Diagnose setup issues and get recommendations.

```bash
devenv doctor

# Check specific directory
devenv doctor --target-dir ~/projects/my-project
```

### `devenv unlink`

Remove Cursor rules symlink from a project.

```bash
devenv unlink

# Unlink specific directory
devenv unlink --target-dir ~/projects/my-project
```

## Usage Workflow

### Setting Up a New Project

```bash
cd ~/projects/new-project
devenv setup
```

The `.cursor` directory is now symlinked to your central rules.

### Setting Up Remote Workspace (Anyscale, etc.)

```bash
# SSH into remote machine
ssh user@remote-host

# Install devenv
uv pip install git+https://github.com/nehiljain/devenv.git

# Setup in workspace
cd /path/to/workspace
devenv setup
```

### Updating Rules Everywhere

Edit rules in the devenv repository:

```bash
cd ~/devenv  # or wherever you cloned it
# Edit cursor-rules/commands/*.md or cursor-rules/rules/**/*.mdc
git add .
git commit -m "Update rules"
git push
```

On any machine with devenv installed:

```bash
cd ~/devenv
git pull
```

All symlinked projects immediately see the updates.

## Repository Structure

```
devenv/
├── cursor-rules/           # Central Cursor configuration
│   ├── commands/          # Custom Cursor commands (*.md)
│   └── rules/             # Cursor rules (*.mdc)
│       └── writing/       # Writing-specific rules
├── devenv/                # Python package
│   ├── __init__.py
│   ├── cli.py            # CLI commands
│   └── setup.py          # Core symlink logic
├── pyproject.toml        # Package configuration
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## How It Works

DevEnv creates symbolic links from your project's `.cursor` directory to the central `cursor-rules` directory in the devenv installation:

```
~/projects/my-project/.cursor → /path/to/devenv/cursor-rules
```

When Cursor reads configuration from `.cursor`, it follows the symlink to the central location. When you update the central rules, all projects using symlinks see the changes immediately.

## Adding Your Own Rules

### Adding Commands

Create a new `.md` file in `cursor-rules/commands/`:

```bash
cd ~/devenv/cursor-rules/commands
vim my-new-command.md
```

### Adding Rules

Create a new `.mdc` file in `cursor-rules/rules/`:

```bash
cd ~/devenv/cursor-rules/rules
mkdir -p my-category
vim my-category/my-rule.mdc
```

## Troubleshooting

### "cursor-rules directory not found"

The package may not be installed correctly. Try reinstalling:

```bash
uv pip uninstall devenv
uv pip install git+https://github.com/nehiljain/devenv.git
```

### ".cursor directory already exists"

Use `--force` to backup and replace:

```bash
devenv setup --force
```

Your existing `.cursor` will be backed up with a timestamp.

### "Not a symlink"

If `.cursor` exists as a regular directory, use:

```bash
devenv setup --force
```

### Check diagnostics

Run the doctor command to identify issues:

```bash
devenv doctor
```

## Tips

### Multiple Machines

Install devenv on each machine, then setup projects individually:

```bash
# On machine 1
uv pip install git+https://github.com/nehiljain/devenv.git
cd ~/projects/project-a
devenv setup

# On machine 2
uv pip install git+https://github.com/nehiljain/devenv.git
cd ~/workspace/project-b
devenv setup
```

Edit rules once, push to GitHub, pull on other machines.

### Checking What's Linked

Use `devenv status` to see if a project is properly linked:

```bash
cd ~/projects/my-project
devenv status
```

### Unlinking

To stop using central rules:

```bash
devenv unlink
```

This removes the symlink but doesn't delete the central rules.

## Contributing

This is a personal tool, but feel free to fork and adapt for your own needs.

## License

MIT

