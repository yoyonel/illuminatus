import datetime
import lmj.cli
import lmj.photos
import os
import subprocess
import sys
import traceback

cmd = lmj.cli.add_command('import')
cmd.add_argument('--tag', default=[], nargs='+', metavar='TAG',
                 help='apply these TAGs to all imported photos')
cmd.add_argument('source', nargs='+', metavar='PATH',
                 help='import photos from these PATHs')
cmd.set_defaults(mod=sys.modules[__name__])

logging = lmj.cli.get_logger(__name__)


def import_one(path, tags):
    exif, = lmj.photos.parse(subprocess.check_output(['exiftool', '-json', path]))

    stamp = datetime.datetime.now()
    for key in 'DateTimeOriginal CreateDate ModifyDate FileModifyDate'.split():
        stamp = exif.get(key)
        if stamp:
            stamp = datetime.datetime.strptime(stamp[:19], '%Y:%m:%d %H:%M:%S')
            break

    p = lmj.photos.insert(path)
    p.exif = exif
    p.meta = dict(stamp=stamp, user_tags=list(tags), thumb=p.thumb_path)
    p.make_thumbnails(sizes=[('img', 700)])

    lmj.photos.update(p)


def main(args):
    errors = []
    for src in args.source:
        for base, dirs, files in os.walk(src):
            dots = [n for n in dirs if n.startswith('.')]
            [dirs.remove(d) for d in dots]
            for name in files:
                if name.startswith('.'):
                    continue
                _, ext = os.path.splitext(name)
                if ext.lower()[1:] in 'gif jpg jpeg png tif tiff':
                    path = os.path.join(base, name)
                    if lmj.photos.exists(path):
                        logging.info('= %s', path)
                        continue
                    try:
                        import_one(path, args.tag)
                        logging.warn('+ %s', path)
                    except:
                        _, exc, tb = sys.exc_info()
                        errors.append((path, exc, traceback.format_tb(tb)))
    for path, exc, tb in errors:
        logging.error('! %s %s', path, exc)#, ''.join(tb))
