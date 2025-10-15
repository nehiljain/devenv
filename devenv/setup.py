"""Core setup logic for symlinking Cursor rules and configuration."""

from pathlib import Path
import os
import shutil
from datetime import datetime
from typing import Tuple


def get_devenv_root() -> Path:
    """Find devenv installation directory containing cursor-rules."""
    # Get the package installation directory
    package_dir = Path(__file__).parent.parent
    cursor_rules_dir = package_dir / "cursor-rules"
    
    if not cursor_rules_dir.exists():
        raise FileNotFoundError(
            f"cursor-rules directory not found at {cursor_rules_dir}. "
            "The package may not be installed correctly."
        )
    
    return package_dir


def setup_cursor_rules(target_dir: Path, force: bool = False) -> Tuple[bool, str]:
    """
    Create symlink for .cursor directory in target project.
    
    Args:
        target_dir: Target project directory
        force: If True, backup existing .cursor and create new symlink
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    target_dir = Path(target_dir).resolve()
    target_cursor = target_dir / ".cursor"
    
    try:
        source_cursor = get_devenv_root() / "cursor-rules"
    except FileNotFoundError as e:
        return False, str(e)
    
    # Check if already symlinked correctly
    if target_cursor.is_symlink():
        current_target = target_cursor.resolve()
        if current_target == source_cursor:
            return True, f"Already linked to {source_cursor}"
        else:
            if not force:
                return False, (
                    f".cursor is symlinked to {current_target}, not {source_cursor}. "
                    "Use --force to replace."
                )
            # Remove old symlink
            target_cursor.unlink()
    
    # Check if .cursor exists as regular directory
    elif target_cursor.exists():
        if not force:
            return False, (
                f".cursor directory already exists at {target_cursor}. "
                "Use --force to backup and replace."
            )
        
        # Backup existing directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = target_dir / f".cursor.backup.{timestamp}"
        shutil.move(str(target_cursor), str(backup_path))
        message_suffix = f" (backed up to {backup_path.name})"
    else:
        message_suffix = ""
    
    # Create symlink
    try:
        os.symlink(source_cursor, target_cursor)
        return True, f"Linked .cursor to {source_cursor}{message_suffix}"
    except OSError as e:
        return False, f"Failed to create symlink: {e}"


def check_setup_status(target_dir: Path) -> dict:
    """
    Check the current setup status of a directory.
    
    Returns:
        Dictionary with status information
    """
    target_dir = Path(target_dir).resolve()
    target_cursor = target_dir / ".cursor"
    
    status = {
        "target_dir": str(target_dir),
        "cursor_exists": target_cursor.exists(),
        "cursor_is_symlink": target_cursor.is_symlink(),
        "cursor_target": None,
        "correctly_linked": False,
    }
    
    try:
        devenv_root = get_devenv_root()
        expected_source = devenv_root / "cursor-rules"
        status["devenv_root"] = str(devenv_root)
        status["expected_source"] = str(expected_source)
    except FileNotFoundError:
        status["devenv_root"] = None
        status["expected_source"] = None
        return status
    
    if target_cursor.is_symlink():
        status["cursor_target"] = str(target_cursor.resolve())
        status["correctly_linked"] = (
            target_cursor.resolve() == expected_source
        )
    
    return status


def remove_cursor_symlink(target_dir: Path) -> Tuple[bool, str]:
    """
    Remove .cursor symlink from target directory.
    
    Args:
        target_dir: Target project directory
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    target_dir = Path(target_dir).resolve()
    target_cursor = target_dir / ".cursor"
    
    if not target_cursor.exists():
        return True, "No .cursor directory found"
    
    if not target_cursor.is_symlink():
        return False, ".cursor is not a symlink, won't remove"
    
    try:
        target_cursor.unlink()
        return True, f"Removed symlink at {target_cursor}"
    except OSError as e:
        return False, f"Failed to remove symlink: {e}"

