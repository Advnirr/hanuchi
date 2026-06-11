desktop_file = 'hanuchi.desktop'
metainfo_file = 'com.github.hanuchi.metainfo.xml'

install_data(desktop_file,
  install_dir: get_option('datadir') / 'applications',
)

install_data('icons/hicolor/scalable/apps/hanuchi.svg',
  install_dir: get_option('datadir') / 'icons/hicolor/scalable/apps',
)

install_data(metainfo_file,
  install_dir: get_option('datadir') / 'metainfo',
)

# Data-file validation (run with `meson test`).
desktop_file_validate = find_program('desktop-file-validate', required: false)
if desktop_file_validate.found()
  test('validate-desktop',
    desktop_file_validate,
    args: [meson.current_source_dir() / desktop_file],
  )
endif

appstreamcli = find_program('appstreamcli', required: false)
if appstreamcli.found()
  test('validate-metainfo',
    appstreamcli,
    args: ['validate', '--no-net', '--explain', meson.current_source_dir() / metainfo_file],
  )
endif
