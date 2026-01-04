# Dotfiles

Configuration files for Windows development environment.

## Contents

- `.bash_profile` - Bash login shell config (sources `.bashrc`)
- `.bashrc` - Bash configuration (yazi shell wrapper)
- `.gitconfig` - Git configuration (aliases, LF line endings, defaults)
- `scoop-packages.json` - Scoop package list
- `vscode-settings.json` - VSCode settings (LF line endings, Git Bash default)
- `vscode-keybindings.json` - VSCode keybindings

## Setup

```bash
# Install scoop packages
scoop import dotfiles/scoop-packages.json

# Copy configs
cp -f dotfiles/.bash_profile ~/
cp -f dotfiles/.bashrc ~/
cp -f dotfiles/.gitconfig ~/
cp -f dotfiles/vscode-settings.json "$APPDATA/Code/User/settings.json"
cp -f dotfiles/vscode-keybindings.json "$APPDATA/Code/User/keybindings.json"

# Reload
source ~/.bashrc
```

Verify:

```bash
git config --list  # Should show your aliases
type y             # Should show yazi wrapper function
```

## Maintenance

Update repo after config changes:

```bash
# Update scoop packages list
scoop export > dotfiles/scoop-packages.json

# Copy configs back
cp -f ~/.bash_profile dotfiles/
cp -f ~/.bashrc dotfiles/
cp -f ~/.gitconfig dotfiles/
cp -f "$APPDATA/Code/User/settings.json" dotfiles/vscode-settings.json
cp -f "$APPDATA/Code/User/keybindings.json" dotfiles/vscode-keybindings.json
```

## TODO

- try chezmoi? https://github.com/twpayne/chezmoi
- consolidate with linux machine config? https://github.com/hi-ogawa/config