project('hanuchi',
  version: '2.1.0',
  license: 'MIT',
  meson_version: '>= 0.59.0',
)

gnome = import('gnome')

conf = configuration_data()
conf.set('VERSION', meson.project_version())

configure_file(
  input: 'src/hanuchi',
  output: 'hanuchi',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x',
)

install_data('LICENSE',
  install_dir: get_option('datadir') / 'licenses' / meson.project_name(),
)

subdir('data')

# Only matters for `ninja install`; distro packages refresh these caches through
# their own triggers, so a build host without the tools is fine.
icon_cache = find_program('gtk4-update-icon-cache', 'gtk-update-icon-cache', required: false)
desktop_db = find_program('update-desktop-database', required: false)
gnome.post_install(
  gtk_update_icon_cache: icon_cache.found(),
  update_desktop_database: desktop_db.found(),
)
