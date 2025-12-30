# Maintainer: User <user@localhost>
pkgname=hanuchi
pkgver=1.3
pkgrel=1
pkgdesc="Native GUI for Hamachi"
arch=('any')
license=('MIT')
# Добавили libayatana-appindicator в зависимости
depends=('python' 'gtk4' 'libadwaita' 'python-gobject' 'logmein-hamachi' 'libayatana-appindicator')
source=('hanuchi.py'
        'hanuchi.desktop'
        'hanuchi.svg')
md5sums=('SKIP' 'SKIP' 'SKIP')

package() {
    install -Dm755 "hanuchi.py" "${pkgdir}/usr/bin/hanuchi"
    install -Dm644 "hanuchi.desktop" "${pkgdir}/usr/share/applications/hanuchi.desktop"
    install -Dm644 "hanuchi.svg" "${pkgdir}/usr/share/icons/hicolor/scalable/apps/hanuchi.svg"
}
