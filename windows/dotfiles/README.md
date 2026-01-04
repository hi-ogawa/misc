# Dotfiles

Configuration files for Windows development environment, managed with [chezmoi](https://www.chezmoi.io/).

## What Gets Configured

- **Bash** - Shell wrapper for yazi file manager
- **Git** - User info, aliases, line ending settings
- **VSCode** - LF line endings, Git Bash terminal, keybindings
- **Scoop packages** - gh (GitHub CLI), yazi (terminal file manager)

## Quick Setup

One command to install everything:

```bash
scoop install chezmoi
chezmoi init --apply ~/code/personal/misc/windows/dotfiles
```

This will:
1. Install scoop packages (gh, yazi)
2. Deploy dotfiles (.bash_profile, .bashrc, .gitconfig)
3. Configure VSCode settings

Verify:

```bash
git config --list  # Should show aliases
type y             # Should show yazi wrapper
```

## Daily Usage

```bash
# Check what would change
chezmoi diff

# Apply any updates from the repo
chezmoi apply

# Edit a config file (opens in $EDITOR)
chezmoi edit ~/.bashrc

# See what chezmoi is managing
chezmoi managed
```

## Making Changes

When you edit configs directly (e.g., in VSCode or ~/.bashrc):

```bash
# Add changes back to chezmoi source
chezmoi add ~/.bashrc
chezmoi add "$APPDATA/Code/User/settings.json"

# Or use chezmoi edit to edit the source directly
chezmoi edit ~/.gitconfig

# Commit changes to git
cd ~/code/personal/misc/windows
git add dotfiles/
git commit -m "update dotfiles"
```

## File Structure

```
dotfiles/
├── dot_bash_profile              → ~/.bash_profile
├── dot_bashrc                    → ~/.bashrc
├── dot_gitconfig                 → ~/.gitconfig
├── run_once_before_install-packages.sh.tmpl   # Installs scoop packages
├── run_onchange_after_vscode-settings.sh.tmpl # Syncs VSCode configs
├── vscode-settings.json          # Source for VSCode settings
├── vscode-keybindings.json       # Source for VSCode keybindings
└── .chezmoiignore                # Files to ignore
```

## Next Steps

- Cross-platform support with templates (Linux/macOS)
- Consolidate with linux machine config: https://github.com/hi-ogawa/config
