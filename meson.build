project('hanuchi',
  version: '2.0.1',
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

gnome.post_install(
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
