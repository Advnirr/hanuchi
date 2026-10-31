Name:           hanuchi
Version:        2.0.1
Release:        1%{?dist}
Summary:        Minimalist GTK4 frontend for LogMeIn Hamachi
License:        MIT
URL:            https://github.com/Advnirr/hanuchi
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  meson

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       polkit
# Not in the Fedora repos; comes from vpn.net.
Recommends:     logmein-hamachi

%description
Shows your Hamachi networks and who is online in them, joins, creates, leaves
and deletes networks, and starts the logmein-hamachi service through polkit.

%prep
%autosetup -n hanuchi-%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/hanuchi
%{_datadir}/applications/hanuchi.desktop
%{_datadir}/icons/hicolor/scalable/apps/hanuchi.svg
%{_datadir}/metainfo/com.github.hanuchi.metainfo.xml
