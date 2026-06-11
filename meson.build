project('hanuchi',
  version: '2.0.0',
  license: 'MIT',
  meson_version: '>= 0.59.0',
)

gnome = import('gnome')

install_data('src/hanuchi',
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x',
)

install_data('LICENSE',
  install_dir: get_option('datadir') / 'licenses' / meson.project_name(),
)

subdir('data')

gnome.post_install(
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
