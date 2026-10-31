# Hanuchi

**Minimalist GTK4/Libadwaita frontend for LogMeIn Hamachi.**

<p align="left">
  <a href="https://github.com/Advnirr/hanuchi/releases">
    <img src="https://img.shields.io/badge/release-v2.0.1-007EC6?style=flat-square" alt="Release">
  </a>
  <a href="https://aur.archlinux.org/packages/hanuchi">
    <img src="https://img.shields.io/aur/version/hanuchi?style=flat-square&label=AUR&color=1793D1" alt="AUR">
  </a>
  <a href="https://github.com/Advnirr/hanuchi/actions/workflows/checks.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/Advnirr/hanuchi/checks.yml?branch=main&style=flat-square&label=checks" alt="Checks">
  </a>
  <a href="https://github.com/Advnirr/hanuchi/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-FF5722?style=flat-square" alt="License">
  </a>
</p>

![Hanuchi Screenshot](assets/screenshot.png)

Hanuchi is a lightweight, utility-first GUI for managing LogMeIn Hamachi networks on Linux.
Designed for modern GNOME environments (Wayland supported), strictly following the philosophy of keeping the tool clean, native, and bloat-free.

## Features
* **Native Experience:** Written in Python using GTK4 and Libadwaita.
* **System Integration:** Controls the `logmein-hamachi` systemd service automatically via PolicyKit.
* **Zero-config Setup:** Automatically starts the daemon and registers your node with Hamachi on first launch — no terminal required.
* **Localization:** English / Russian

## Requirements
* Python 3.10+
* `logmein-hamachi` (installed and configured)
* `gtk4`, `libadwaita` (>= 1.2), `python-gobject`
* `meson`, `ninja` (build-time only)

## Installation

### Arch Linux / CachyOS / Manjaro
You can install Hanuchi using the included `PKGBUILD`:

```bash
cd pkg/
makepkg -si
```

Also you can install Hanuchi from AUR using Yay:

```bash
yay -S hanuchi
```

### Debian / Ubuntu
Download `hanuchi_<version>_all.deb` from [Releases](https://github.com/Advnirr/hanuchi/releases) and install it:

```bash
sudo apt install ./hanuchi_*_all.deb
```

### Fedora
Download the `.rpm` from [Releases](https://github.com/Advnirr/hanuchi/releases) and install it:

```bash
sudo dnf install ./hanuchi-*.noarch.rpm
```

Hamachi itself is not in the Debian or Fedora repos: install `logmein-hamachi` from [vpn.net](https://vpn.net/linux) first.

You can also build both packages with `tools/build-packages.sh`. It needs `meson`, `dpkg-deb` and `rpmbuild` and puts the files in `dist/`.

### From Source (Any Distro)
Hanuchi uses the [Meson](https://mesonbuild.com/) build system. Clone the repository and build:

```bash
git clone https://github.com/Advnirr/hanuchi.git
cd hanuchi
meson setup build --prefix=/usr
ninja -C build
sudo ninja -C build install
```

## Removal

### Arch Based Distributions
Remove using the pacman package manager.

```bash
sudo pacman -R hanuchi
```

### Debian / Ubuntu / Fedora

```bash
sudo apt remove hanuchi    # Debian / Ubuntu
sudo dnf remove hanuchi    # Fedora
```

### Built From Source
From the build directory created during installation:

```bash
sudo ninja -C build uninstall
```

## Support

If Hanuchi made Hamachi on Linux less painful, you can support continued
development directly:

**USDT** · TON network

```
UQDFela8stCZykNL2cLw2erPkzjAgSf-GLXoJuiTEmEckTNB
```

## License
MIT License.
