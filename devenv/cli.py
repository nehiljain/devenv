"""Main CLI entrypoint for devenv setup tool."""

import click
from pathlib import Path
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from .setup import (
    setup_cursor_rules,
    check_setup_status,
    remove_cursor_symlink,
    get_devenv_root,
)

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Personal development environment setup tool.
    
    Manage Cursor rules and development tools across projects.
    """
    pass


@main.command()
@click.option(
    '--target-dir',
    default='.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help='Target project directory (default: current directory)'
)
@click.option(
    '--force',
    is_flag=True,
    help='Force setup, backing up existing .cursor directory if needed'
)
def setup(target_dir, force):
    """Setup Cursor rules in a project directory.
    
    Creates a symlink from .cursor/ to the central cursor-rules directory.
    All projects linked this way will share the same rules and stay in sync.
    """
    target_path = Path(target_dir).resolve()
    
    console.print(f"\n[bold cyan]Setting up devenv in:[/bold cyan] {target_path}")
    
    # Setup cursor rules
    success, message = setup_cursor_rules(target_path, force=force)
    
    if success:
        console.print(f"[green]✓[/green] {message}")
        console.print("\n[bold green]Setup complete![/bold green]")
        console.print("\nYour .cursor directory is now symlinked to central rules.")
        console.print("Run [cyan]devenv status[/cyan] to verify the setup.\n")
    else:
        console.print(f"[red]✗[/red] {message}", style="red")
        if not force and "Use --force" in message:
            console.print("\n[yellow]Tip:[/yellow] Run with --force to backup and replace.\n")
        sys.exit(1)


@main.command()
@click.option(
    '--target-dir',
    default='.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help='Target project directory (default: current directory)'
)
def status(target_dir):
    """Check current setup status.
    
    Shows whether Cursor rules are properly linked and displays
    configuration information.
    """
    target_path = Path(target_dir).resolve()
    
    console.print(f"\n[bold cyan]Checking status for:[/bold cyan] {target_path}\n")
    
    status_info = check_setup_status(target_path)
    
    # Create status table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Target Directory", status_info["target_dir"])
    table.add_row("DevEnv Root", status_info.get("devenv_root", "[red]Not found[/red]"))
    
    if status_info.get("expected_source"):
        table.add_row("Expected Source", status_info["expected_source"])
    
    # Cursor status
    if status_info["cursor_exists"]:
        if status_info["cursor_is_symlink"]:
            table.add_row(".cursor Status", "[yellow]Symlink[/yellow]")
            table.add_row("Linked To", status_info.get("cursor_target", "[red]Unknown[/red]"))
            
            if status_info["correctly_linked"]:
                table.add_row("Correctly Linked", "[green]✓ Yes[/green]")
            else:
                table.add_row("Correctly Linked", "[red]✗ No[/red]")
        else:
            table.add_row(".cursor Status", "[yellow]Regular Directory[/yellow]")
            table.add_row("Correctly Linked", "[red]✗ No[/red]")
    else:
        table.add_row(".cursor Status", "[red]Not Found[/red]")
        table.add_row("Correctly Linked", "[red]✗ No[/red]")
    
    console.print(table)
    
    # Summary message
    if status_info["correctly_linked"]:
        console.print("\n[bold green]✓ Setup is correct![/bold green]")
        console.print("Your .cursor rules are properly linked.\n")
    else:
        console.print("\n[bold yellow]⚠ Setup needs attention[/bold yellow]")
        if not status_info["cursor_exists"]:
            console.print("Run [cyan]devenv setup[/cyan] to create the symlink.\n")
        elif not status_info["cursor_is_symlink"]:
            console.print("Run [cyan]devenv setup --force[/cyan] to backup and link.\n")
        else:
            console.print("Run [cyan]devenv setup --force[/cyan] to fix the link.\n")


@main.command()
@click.option(
    '--target-dir',
    default='.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help='Target project directory (default: current directory)'
)
@click.confirmation_option(prompt='Are you sure you want to remove the .cursor symlink?')
def unlink(target_dir):
    """Remove .cursor symlink from a project.
    
    This will unlink the project from central rules but won't
    delete the central rules themselves.
    """
    target_path = Path(target_dir).resolve()
    
    console.print(f"\n[bold cyan]Unlinking from:[/bold cyan] {target_path}")
    
    success, message = remove_cursor_symlink(target_path)
    
    if success:
        console.print(f"[green]✓[/green] {message}\n")
    else:
        console.print(f"[red]✗[/red] {message}\n", style="red")
        sys.exit(1)


@main.command()
def info():
    """Display devenv installation information.
    
    Shows where devenv is installed and where cursor-rules are located.
    """
    console.print("\n[bold cyan]DevEnv Installation Info[/bold cyan]\n")
    
    try:
        devenv_root = get_devenv_root()
        cursor_rules = devenv_root / "cursor-rules"
        
        table = Table(show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("DevEnv Root", str(devenv_root))
        table.add_row("Cursor Rules", str(cursor_rules))
        table.add_row("Rules Exist", "[green]✓ Yes[/green]" if cursor_rules.exists() else "[red]✗ No[/red]")
        
        console.print(table)
        
        # Count rules and commands
        if cursor_rules.exists():
            commands_dir = cursor_rules / "commands"
            rules_dir = cursor_rules / "rules"
            
            num_commands = len(list(commands_dir.glob("*.md"))) if commands_dir.exists() else 0
            num_rules = len(list(rules_dir.rglob("*.mdc"))) if rules_dir.exists() else 0
            
            console.print(f"\n[bold]Available Resources:[/bold]")
            console.print(f"  Commands: {num_commands}")
            console.print(f"  Rules: {num_rules}\n")
        
    except FileNotFoundError as e:
        console.print(f"[red]✗[/red] {e}\n", style="red")
        sys.exit(1)


@main.command()
@click.option(
    '--target-dir',
    default='.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help='Target project directory (default: current directory)'
)
def doctor(target_dir):
    """Diagnose setup issues and provide recommendations.
    
    Runs checks to identify common problems with the setup.
    """
    target_path = Path(target_dir).resolve()
    
    console.print(f"\n[bold cyan]Running diagnostics for:[/bold cyan] {target_path}\n")
    
    issues = []
    warnings = []
    checks = []
    
    # Check 1: DevEnv installation
    try:
        devenv_root = get_devenv_root()
        checks.append(("DevEnv installed", True, None))
        
        # Check 2: Cursor rules exist
        cursor_rules = devenv_root / "cursor-rules"
        if cursor_rules.exists():
            checks.append(("Cursor rules found", True, None))
        else:
            checks.append(("Cursor rules found", False, "cursor-rules directory missing"))
            issues.append("Cursor rules directory not found at expected location")
        
    except FileNotFoundError:
        checks.append(("DevEnv installed", False, "Installation not found"))
        issues.append("DevEnv installation appears corrupted")
    
    # Check 3: Target directory setup
    status_info = check_setup_status(target_path)
    
    if status_info["correctly_linked"]:
        checks.append(("Cursor rules linked", True, None))
    elif status_info["cursor_exists"]:
        if status_info["cursor_is_symlink"]:
            checks.append(("Cursor rules linked", False, "Linked to wrong location"))
            issues.append(f".cursor is linked to {status_info['cursor_target']} instead of {status_info.get('expected_source', 'expected location')}")
        else:
            checks.append(("Cursor rules linked", False, "Not a symlink"))
            warnings.append(".cursor exists as a regular directory, not a symlink")
    else:
        checks.append(("Cursor rules linked", False, "Not set up"))
        warnings.append(".cursor directory not found in target")
    
    # Display results
    for check_name, passed, detail in checks:
        if passed:
            console.print(f"[green]✓[/green] {check_name}")
        else:
            console.print(f"[red]✗[/red] {check_name}" + (f": {detail}" if detail else ""))
    
    console.print()
    
    # Report issues
    if issues:
        console.print("[bold red]Issues Found:[/bold red]")
        for issue in issues:
            console.print(f"  • {issue}")
        console.print()
    
    if warnings:
        console.print("[bold yellow]Warnings:[/bold yellow]")
        for warning in warnings:
            console.print(f"  • {warning}")
        console.print()
    
    # Recommendations
    if issues or warnings:
        console.print("[bold cyan]Recommendations:[/bold cyan]")
        if not status_info["correctly_linked"]:
            if status_info["cursor_exists"] and not status_info["cursor_is_symlink"]:
                console.print("  → Run [cyan]devenv setup --force[/cyan] to backup and link")
            else:
                console.print("  → Run [cyan]devenv setup[/cyan] to create the symlink")
        console.print()
    else:
        console.print("[bold green]✓ All checks passed![/bold green]\n")


if __name__ == "__main__":
    main()

