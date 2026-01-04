# Dotfiles

Configuration files for Windows development environment.

## Contents

- **`.bash_profile`** - Bash login shell config (sources `.bashrc`)
- **`.bashrc`** - Bash configuration (yazi shell wrapper)
- **`.gitconfig`** - Git configuration (aliases, LF line endings, defaults)
- **`scoop-packages.json`** - Scoop package list (can be imported with `scoop import`)

## About Bash Profiles

**Git Bash on Windows:**
- Each new Git Bash window is a **login shell**
- Login shells execute `.bash_profile` (not `.bashrc`)
- The `.bash_profile` sources `.bashrc` for you
- **Result:** Put your configs in `.bashrc`, it will be loaded automatically

**Why this matters:**
- `.bash_profile` - executed once per login shell (each Git Bash window)
- `.bashrc` - executed for interactive shells (sourced by `.bash_profile`)
- Standard pattern: Keep customizations in `.bashrc`, let `.bash_profile` source it

## Manual Setup (Copy/Paste)

### 1. Install scoop

```powershell
# Run in PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

### 2. Install scoop packages

```powershell
# Option A: Import from JSON
scoop import scoop-packages.json

# Option B: Manual install
scoop install yazi
```

### 3. Copy dotfiles

```bash
# Run in Git Bash or PowerShell
cp dotfiles/.bash_profile ~/
cp dotfiles/.bashrc ~/
cp dotfiles/.gitconfig ~/
```

### 4. Reload shell

```bash
# Git Bash
source ~/.bashrc

# Or just restart your terminal
```

## Verification

```bash
# Check git config
git config --list

# Check yazi wrapper function
type y

# Test yazi
y
```

## Future: Automated Setup with chezmoi

For full automation across machines, consider using [chezmoi](https://www.chezmoi.io/):

```bash
# Install chezmoi
winget install twpayne.chezmoi

# Initialize from this repo (when ready)
chezmoi init https://github.com/hi-ogawa/windows-setup
chezmoi apply
```

This would handle:
- Symlinks or copies of dotfiles
- Template support for machine-specific values
- Automatic updates when repo changes
- Cross-platform support (Windows/Linux)

## Maintenance

### Update scoop-packages.json

When you install new scoop packages:

```bash
scoop export > dotfiles/scoop-packages.json
```

### Update dotfiles

After changing your configs:

```bash
cp ~/.bash_profile dotfiles/
cp ~/.bashrc dotfiles/
cp ~/.gitconfig dotfiles/
```

Then commit the changes to this repo.
