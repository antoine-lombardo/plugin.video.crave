from genericpath import isfile
from shutil import copytree, rmtree, make_archive, move
from os.path import isdir, join
import fnmatch
import os


def include_patterns(*patterns):
    def _ignore_patterns(path, all_names):
        # Determine names which match one or more patterns (that shouldn't be
        # ignored).
        keep = (name for pattern in patterns
                for name in fnmatch.filter(all_names, pattern))
        # Ignore file names which *didn't* match any of the patterns given that
        # aren't directory names.
        dir_names = (name for name in all_names if isdir(join(path, name)))
        return set(all_names) - set(keep) - set(dir_names)
    return _ignore_patterns


def remove_empty_folders(path_abs):
    walk = list(os.walk(path_abs))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            os.rmdir(path)


plugin_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
tmp_dir = 'tmp'
pack_dir = 'pack'
plugin_dir = join(pack_dir, plugin_name)

if isdir(tmp_dir):
    rmtree(tmp_dir)

if isdir(pack_dir):
    rmtree(pack_dir)

copytree('./', tmp_dir,
         ignore=include_patterns('*.py', '*.xml', '*.png', '*.jpg'))

remove_empty_folders(tmp_dir)

move(tmp_dir, plugin_dir)

# Delete empty folders
remove_empty_folders(tmp_dir)

if isfile(plugin_name + '.zip'):
    os.remove(plugin_name + '.zip')

make_archive(plugin_name, 'zip', pack_dir)

if isdir(tmp_dir):
    rmtree(tmp_dir)

if isdir(pack_dir):
    rmtree(pack_dir)
