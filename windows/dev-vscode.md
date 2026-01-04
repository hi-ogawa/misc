# VSCode Setup (Windows)

Windows-specific VSCode configuration and best practices.

## Config File Locations

**Windows paths:**
- Settings: `%APPDATA%\Code\User\settings.json`
- Keybindings: `%APPDATA%\Code\User\keybindings.json`
- Extensions: `%USERPROFILE%\.vscode\extensions\`

## Settings

```json
{
  // Line endings - CRITICAL: force LF for Git compatibility
  "files.eol": "\n",

  // Terminal - choose your default shell
  "terminal.integrated.defaultProfile.windows": "Git Bash",  // or "PowerShell"
}
```

## Notes

**Windows Defender performance:**
Can slow file watching. Consider exclusions:
- Code directory: `C:\Users\<user>\code\`
- VSCode: `C:\Program Files\Microsoft VS Code\`
- npm: `%APPDATA%\npm\`

**Line continuation in terminal:**
- Git Bash: `\`
- PowerShell: `` ` ``
