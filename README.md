# new environment install packages

Maintain a `pkgs.toml` file with content like

```toml
[c-compiler]
termux = 'clang'
dnf = 'gcc'
[git]
termux = '.'
pacman = '.'
```

Run `python main.py --pm <pm>`
get packages to install, or `python main.py --sort` to sort `pkgs.toml`.

**NOTE**:
1. package names are matched by regular expression `[A-Za-z0-9_-]+`
2. packages are sorted by lower case
3. package managers are enumerated in Python file `main.py`
4. `'.'` means same as package name

