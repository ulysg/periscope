pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'periscope'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'view/song_thumbnail.blp',
    'view/song_grid.blp',
    'view/window.blp',
    'view/song_player.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('periscope',
  'periscope.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'periscope.in',
  output: 'periscope',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

periscope_sources = [
  '__init__.py',
  'main.py',
  'view/window.py',
  'view/song_grid.py',
  'view/song_thumbnail.py',
  'view/song_player.py',
  'model/config.py',
  'model/async_loop.py',
  'model/player.py',
  'model/api/subsonic.py',
  'model/api/errors.py',
  'model/api/medias.py'
]

install_data(periscope_sources, install_dir: moduledir)
