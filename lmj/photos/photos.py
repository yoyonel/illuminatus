import cv2
import datetime
import json
import os
import PIL.Image


def parse(x):
    return json.loads(x)

def stringify(x):
    h = lambda z: z.isoformat() if isinstance(z, datetime.datetime) else None
    return json.dumps(x, default=h)


class Photo(object):
    def __init__(self, id=-1, path='', meta=None, exif=None, ops=None):
        self.id = id
        self.path = path
        self.meta = parse(meta or '{}')
        self.exif = parse(exif or '{}')
        self.ops = parse(ops or '[]')

    @property
    def tag_set(self):
        return (self.datetime_tag_set |
                self.user_tag_set |
                self.geo_tag_set |
                self.exif_tag_set)

    @property
    def user_tag_set(self):
        return set(self.meta.get('user_tags', []))

    @property
    def geo_tag_set(self):
        return set()

    @property
    def datetime_tag_set(self):
        if not self.stamp:
            return set()

        def ordinal(n):
            s = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            if 10 < n < 20: s = 'th'
            return '%d%s' % (n, s)

        return set([self.stamp.strftime('%Y'),
                    self.stamp.strftime('%B').lower(),
                    self.stamp.strftime('%A').lower(),
                    ordinal(int(self.stamp.strftime('%d'))),
                    self.stamp.strftime('%I%p').lower().strip('0'),
                    ])

    @property
    def exif_tag_set(self):
        return set()

    @property
    def stamp(self):
        stamp = self.meta.get('stamp')
        if not stamp:
            return None
        if isinstance(stamp, datetime.datetime):
            return stamp
        return datetime.datetime.strptime(stamp, '%Y-%m-%dT%H:%M:%S')

    @property
    def thumb_path(self):
        id = '%08x' % self.id
        return os.path.join(id[:-3], '%s.jpg' % id[-3:])

    def to_dict(self):
        return dict(id=self.id,
                    path=self.path,
                    stamp=self.stamp,
                    meta=self.meta,
                    thumb=self.thumb_path,
                    tags=list(self.tag_set))

    def make_thumbnails(self, sizes=(('full', 1000), ('thumb', 200)), replace=False):
        import lmj.photos
        base = os.path.dirname(lmj.photos.DB)
        img = self.get_image()
        for name, size in sorted(sizes, key=lambda x: -x[1]):
            p = os.path.join(base, name, self.thumb_path)
            dirname = os.path.dirname(p)
            try: os.makedirs(dirname)
            except: pass
            if replace or not os.path.exists(p):
                img.thumbnail((size, size), PIL.Image.ANTIALIAS)
                img.save(p)

    def get_image(self):
        img = PIL.Image.open(self.path)
        if self.exif.get('Orientation') == 'Rotate 90 CW':
            img = img.rotate(-90)
        if self.exif.get('Orientation') == 'Rotate 180':
            img = img.rotate(-180)
        if self.exif.get('Orientation') == 'Rotate 270 CW':
            img = img.rotate(-270)

        for op in self.ops:
            key = op['key']
            if key == 'eq':
                # http://opencvpython.blogspot.com/2013/03/histograms-2-histogram-equalization.html
                img = cv2.equalizeHist(img)
                continue
            if key == 'cr':
                x1, y1, x2, y2 = op['box']
                width, height = img.size
                x1 = int(width * x1)
                y1 = int(height * y1)
                x2 = int(width * x2)
                y2 = int(height * y2)
                img = img.crop([x1, y1, x2, y2])
                continue
            if key == 'ro':
                img = img.rotate(op['degrees'])
                continue
            if key == 'cb':
                img = img.point(op['gamma'], op['alpha'])
                continue
            # TODO: apply more image transforms

        return img

    def add_op(self, key, **op):
        import lmj.photos
        op['key'] = key
        self.ops.append(op)
        lmj.photos.update(self)
