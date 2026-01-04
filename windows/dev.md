# Development Environment

**Prerequisites:** Complete [setup.md](setup.md) first (Git, VSCode, scoop, dotfiles)

## Package Managers: winget vs scoop

### Recommendation: Use scoop for CLI tools, winget for GUI apps

**scoop for CLI dev tools** (Preferred)
- No admin needed
- No terminal restart needed (PATH updates immediately)
- User-local install (`~/scoop/apps/`)
- Better version management

Examples:
```bash
scoop install gh yazi jq ripgrep fd fzf
```

**winget for GUI apps**
- Official Microsoft tool (pre-installed)
- Better for GUI apps
- System-wide install (`C:\Program Files\`)
- Often needs admin, requires terminal restart

Examples:
```bash
winget install Git.Git Microsoft.VisualStudioCode Google.Chrome Microsoft.PowerToys
```

See https://scoop.sh/ for scoop details.

## CLI Tools

Install via scoop:

```bash
scoop install gh           # GitHub CLI
scoop install yazi         # Terminal file manager
scoop install jq           # JSON processor
scoop install ripgrep      # Fast grep alternative (rg)
scoop install fd           # Fast find alternative
```

### Claude Code

```bash
# Via winget (GUI app style)
winget install -e --id Anthropic.ClaudeCode

# Or via scoop (CLI tool style)
scoop install claude-code
```

Verify: `claude --version`

## What does Git for Windows install?

When you run `winget install Git.Git`, you're installing **"Git for Windows"** which includes multiple components:

### 1. Git CLI (`git.exe`)
- The main git command-line tool
- **Added to Windows PATH automatically**
- **Works in PowerShell, Git Bash, CMD - everywhere**
- This is why `git st` works in PowerShell!

### 2. Git Bash (separate shell application)
- A complete Unix-like shell environment based on MSYS2 (modified Cygwin)
- Includes `bash.exe` and many Unix tools
- Installed as a separate GUI application (launchable from Start menu)
- **NOT added to Windows PATH** - only accessible when running Git Bash

### 3. Bundled Unix tools
Located in `C:\Program Files\Git\usr\bin\`:
- File operations: `rm`, `cp`, `mv`, `mkdir`, `cat`, `touch`
- Text processing: `grep`, `sed`, `awk`, `head`, `tail`
- Editors: `vim`, `nano`
- Utilities: `which`, `find`, `diff`, `patch`, `less`, `ssh`, `curl`
- Archives: `tar`, `gzip`

**Key difference:** Only `git.exe` is in Windows PATH. Other Unix tools are NOT, so they only work inside Git Bash shell.

## Shell Environment

**CRITICAL for Linux users:** Windows has **two completely separate shells**. Unix commands like `which`, `grep`, `vim` only work in Git Bash, NOT in PowerShell!

### PowerShell (Windows native shell)
- Default shell in Windows Terminal and VSCode
- Prompt: `PS C:\Users\hiroshi\>`
- Windows-native commands: `Get-ChildItem`, `Copy-Item`, etc.
- Has **some** Unix-like **aliases**: `ls`, `cd`, `cp` (but they're PowerShell cmdlets underneath)
- **Does NOT have**: `which`, `rm`, `grep`, `vim`, most Unix commands
- **Exception:** `git` works here because `git.exe` is in Windows PATH

### Git Bash (Unix-like shell)
- Installed with Git for Windows as a separate application
- Prompt: `hiroshi@COMPUTERNAME MINGW64 ~`
- Real bash shell from Linux/Unix
- All bundled Unix tools available here

### How to access Git Bash

**Option 1:** Launch "Git Bash" application from Start menu

**Option 2:** In VSCode terminal:
- Click the dropdown next to `+` button
- Select "Git Bash" (or "Select Default Profile" → "Git Bash")

**Option 3:** From PowerShell, run:
```powershell
bash
```

### Which shell does Claude Code use?

When Claude Code uses the `Bash` tool, it runs commands in **Git Bash**, not PowerShell. This is why Unix commands work when Claude runs them.

If you're typing commands yourself in VSCode terminal and see the PowerShell prompt (`PS`), Unix commands won't work - switch to Git Bash first.

**Available Unix commands in Git Bash:**
- File operations: `rm`, `ls`, `cp`, `mv`, `mkdir`, `cat`, `touch`
- Text processing: `grep`, `sed`, `awk`, `head`, `tail`
- Editors: `vim`, `nano`
- Utilities: `which`, `find`, `diff`, `patch`, `less`, `ssh`, `curl`
- Archives: `tar`, `gzip`
- Shell: `bash`, `sh`

**Not included by default:**
- `wget` (use `curl` instead, or install via package manager)
- `make` (can install separately)

### Path translation in Git Bash

Git Bash translates between Unix-style and Windows paths:
- Windows `C:\Users\hiroshi\` → Git Bash `/c/Users/hiroshi/`
- Git's internal `/usr/bin/` → Windows `C:\Program Files\Git\usr\bin\`

Examples:
```bash
# Both work in Git Bash
cd /c/Users/hiroshi/code
cd "C:\Users\hiroshi\code"

# Check where commands live
which git     # /mingw64/bin/git
which vim     # /usr/bin/vim
```

### Checking available commands

Use `which <command>` to see if a command exists and where it's located:
```bash
which rm      # /usr/bin/rm
which make    # which: no make in (...)
```

## Integration Friction: Git Bash + Windows Toolchains

**WARNING for Python/Node.js development:** Git Bash works well for git operations, but creates friction when using Windows-installed development tools.

### The Problem

When you install Python and Node.js on Windows:
- You get **Windows native** binaries (`python.exe`, `node.exe`)
- They're added to Windows PATH
- They work in **both** PowerShell and Git Bash
- **But they expect Windows conventions, not Unix**

### Example Friction Points

**Python virtual environments:**
```powershell
# PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# Git Bash
python -m venv .venv
source .venv/Scripts/activate  # Different activation script!
```

**npm/package.json scripts:**
- Scripts with Unix commands (`rm -rf dist`) fail in PowerShell
- Scripts with Windows commands (`rmdir /s /q dist`) fail in Git Bash
- Inconsistent behavior depending on which shell runs the script

**Path handling:**
- Python scripts doing path manipulation - Windows backslashes or Unix forward slashes?
- Tools generating paths - which format?

**Line endings:**
- Git Bash expects LF (Unix)
- Windows tools may generate CRLF
- See [dev-git.md](dev-git.md) for line ending configuration (modern approach: disable autocrlf)

### The Real Decision

**Git Bash is good for:**
- Git operations (`git commit`, `git push`, etc.)
- Basic file manipulation (`rm`, `mv`, `grep`)
- SSH, curl, simple Unix utilities
- **Not good for:** Python/Node.js/high-level toolchain development

**For real development with Python, Node.js, etc., pick one:**

**Option 1: Commit to PowerShell**
- Use Windows native everything
- Learn PowerShell syntax and conventions
- Consistent Windows experience
- Use Git Bash only when you specifically need Unix commands

**Option 2: Go full WSL**
- Install Linux versions of Python, Node.js, etc. inside WSL
- Full Linux environment with proper integration
- Files live in WSL filesystem for performance
- See [dev-wsl.md](dev-wsl.md) for details

**Git Bash middle ground is awkward:** You're mixing Windows programs with a Unix shell, creating constant friction about which shell to use, which path format, which activation script, etc.

## Git Configuration

See **[dev-git.md](dev-git.md)** for detailed git setup instructions.

## Follow-up

- [ ] Install and verify Python + pip
- [ ] Install and verify Node.js + npm
- [ ] Complete GitHub SSH setup
- [ ] Consider version managers (pyenv-win, fnm/nvm-windows) for multi-version support
- [ ] Test Claude Code file operations (read, write, edit)
- [ ] Test git operations with Claude Code
- [ ] Test bash/shell command execution
- [ ] Verify agent can perform automated tasks end-to-end
