# Create DB
```bash
illuminatus --db db/db.sql3 \
--video-format '100,acodec=' \
import "/home/latty/Devel/screenpulse-tests/datas/sp-back02/2038/extract_2038_20170802_000038.mp4"
```

```bash
┏ ✔    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                                 0.06   5.02G    97%   13:42:55  
╰─ illuminatus --db db/db.sql3 --video-format 100,acodec= import "/home/latty/Devel/screenpulse-tests/datas/sp-back02/2038" --tag 2038 --tag sp-back02
```
Import directory containing MP4 videos and tag each entry with support ('2038') and source import ('sp-back02').

# Listing

## Simple filter
```
--db
db/db.sql3
ls
"after:2017-08-02 & before:2017-08-02"
```

# Complex filters
```bash
╰─ illuminatus --db db/db.sql3 ls
00001 2017-08-02T00:00:38+00:00 2017 august 2nd wednesday 12am 2038 sp-back02 /home/latty/Devel/screenpulse-tests/datas/sp-back02/2038/extract_2038_20170802_000038.mp4
```

- Format de la date spécifique à SQLite3:
```bash
╰─ sqlite3 db/db.sql3                                                                            
SQLite version 3.16.2 2017-01-06 16:32:41
Enter ".help" for usage hints.
sqlite> .tables
media        taggedmedia  tags       
sqlite> SELECT stamp FROM media;
2017-08-02T00:00:38+00:00
sqlite> 
```
PS: plus forcément le cas. 'stamp' est une colonne string simple (représentant une date).
Il faut pendant l'utiliser ré-injecter de la sémantique:
```
sqlite> PRAGMA table_info(media);
0|id|INTEGER|1||1
1|path|TEXT|1||0
2|medium|TEXT|1||0
3|stamp|TEXT|0||0
4|fingerprint|TEXT|0||0
5|meta|BLOB|1||0
```

- Filtre plus complexe avec un intervalle de temps:
```bash
╰─ illuminatus --db db/db.sql3 \
    ls \
        "(2038 & sp-back02) & \
        after:2017-08-02T00:00:35 & before:2017-08-02T00:00:40"
```

- Semble supporter les millisecondes:
```bash
┏ ✔    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                                 0.37   0.81G    96%   11:42:35 
─ illuminatus --db db/db.sql3 \
    ls \
        "(2038 & sp-back02) & \
        after:2017-08-02T00:00:35 & before:2017-08-02T00:00:38"
┏ ✔    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                                 0.37   0.81G    96%   11:42:35  
╰─ illuminatus --db db/db.sql3 \
    ls \
        "(2038 & sp-back02) & \
        after:2017-08-02T00:00:35 & before:2017-08-02T00:00:38.50"
00001 2017-08-02T00:00:38+00:00 2017 august 2nd wednesday 12am 2038 sp-back02 /home/latty/Devel/screenpulse-tests/datas/sp-back02/2038/extract_2038_20170802_000038.mp4
```

- Filtre selon les supports, la source des vidéos, et un intervalle de temps (extraits initialement à partir des noms des fichiers vidéos):
```bash
┏ ✔    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                                 6.80   4.86G    97%   14:44:53  
╰─ illuminatus --db db/db.sql3 ls "(2038 | 2006) & sp-back02 & after:2017-08-02T19:00:37.001 & before:2017-08-02T20:00:38.00" --order tag --order id| wc -l
23

┏ ✔    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                                 6.48   4.85G    97%   14:45:09  
╰─ illuminatus --db db/db.sql3 ls "(2038 | 2006) & sp-back02 & after:2017-08-02T19:00:37.001 & before:2017-08-02T20:00:38.00" --order tag --order id                  
00069 2017-08-02T19:45:34+00:00 2017 august 2nd wednesday 7pm 2038 sp-back02 /home/latty/Devel/screenpulse-tests/datas/sp-back02/2038/extract_2038_20170802_194534.mp4
00233 2017-08-02T19:05:35+00:00 2017 august 2nd wednesday 7pm 2038 sp-back02 /home/latty/Devel/screenpulse-tests/datas/sp-back02/2038/extract_2038_20170802_190535.mp4
00234 2017-08-02T19:10:35+00:00 2017 august 2nd wednesday 7pm 2038 sp-back02 /home/latty/Devel/screenpulse-tests/datas/sp-back02/2038/extract_2038_20170802_191035.mp4
...
00406 2017-08-02T19:45:39+00:00 2017 august 2nd wednesday 7pm 2006 sp-back02 /home/latty/Devel/screenpulse-tests/datas/sp-back02/2006/extract_2006_20170802_194539.mp4
00407 2017-08-02T19:50:38+00:00 2017 august 2nd wednesday 8pm 2006 sp-back02 /home/latty/Devel/screenpulse-tests/datas/sp-back02/2006/extract_2006_20170802_195038.mp4
00408 2017-08-02T19:55:36+00:00 2017 august 2nd wednesday 8pm 2006 sp-back02 /home/latty/Devel/screenpulse-tests/datas/sp-back02/2006/extract_2006_20170802_195536.mp4
```

# URL Queries

## Complex filter:

[http://localhost:5555/query/(2038)%20&%20after:2017-08-02T19:00:37.001%20&%20before:2017-08-02T19:10:37.001](http://localhost:5555/query/(2038)%20&%20after:2017-08-02T19:00:37.001%20&%20before:2017-08-02T19:10:37.001)

```bash
┏ ✔    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                                      0.17   3.77G    97%   16:03:54  
╰─ curl http://localhost:5555/query/\(2038\)%20\&%20after:2017-08-02T19:00:37.001%20\&%20before:2017-08-02T19:10:37.001 | python -m json.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed                                   
100  7281  100  7281    0     0   557k      0 --:--:-- --:--:-- --:--:--  592k                                            
{                                          
    "items": [                            
        {                                            
            "filters": [],                               
            "id": 234,                     
            "medium": "video",                      
            "meta": {                                                                                                                                   
                "AudioBitsPerSample": 16,
...
                {                                                
                    "name": "2038",                                                                                                                     
                    "sort": 0,                                                           
                    "source": 255                                                                                                                       
                },                                                                                                                           
                {                                                              
                    "name": "sp-back02",                                                                        
                    "sort": 0,                                                                                            
                    "source": 255          
                }                         
            ]                                        
        }                                                
    ]                                      
}
```

- https://stackoverflow.com/questions/352098/how-can-i-pretty-print-json-in-unix-shell-script

## Thumb directly by (internal) path

[http://localhost:5555/thumb/100x100/0a/93/b7724c38a9a60bc2.mp4](http://localhost:5555/thumb/100x100/0a/93/b7724c38a9a60bc2.mp4)

```bash
┏ ✔    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                                      1.17   1.76G    96%   20:4[2/1941]
╰─ curl http://localhost:5555/thumb/100x100/0a/93/b7724c38a9a60bc2.mp4 | ffprobe -
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current                                                                         
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0ffprobe version 3.2.4-1build2 Copyright (c) 2007-2017 the FFmpeg developers
  built with gcc 6.3.0 (Ubuntu 6.3.0-8ubuntu1) 20170221
  configuration: --prefix=/usr --extra-version=1build2 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --e
nable-gpl --disable-stripping --enable-avresample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libbs2b -
-enable-libcaca --enable-libcdio --enable-libebur128 --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --
enable-libgsm --enable-libmp3lame --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librubberband --enable-libshine --
enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libvpx --enable-li
bwavpack --enable-libwebp --enable-libx265 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-omx --enable-openal --enable-opengl --enable-sdl2 -
-enable-libdc1394 --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libopencv --enable-libx264 --enable-shared
  libavutil      55. 34.101 / 55. 34.101
  libavcodec     57. 64.101 / 57. 64.101
  libavformat    57. 56.101 / 57. 56.101
  libavdevice    57.  1.100 / 57.  1.100
  libavfilter     6. 65.100 /  6. 65.100
  libavresample   3.  1.  0 /  3.  1.  0
  libswscale      4.  2.100 /  4.  2.100
  libswresample   2.  3.100 /  2.  3.100
  libpostproc    54.  1.100 / 54.  1.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'pipe:':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf57.56.101
  Duration: 00:04:58.08, start: 0.000000, bitrate: N/A
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 100x56 [SAR 224:225 DAR 16:9], 18 kb/s, 25 fps, 25 tbr, 12800 tbn, 50 tbc (default
)
    Metadata:
      handler_name    : VideoHandler
```

## Query Thumb by ID:

```bash
┏ ↵ 23|1    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                                1.00   1.99G    96%   20:24:55   
╰─ curl http://localhost:5555/thumb_by_id/221 | ffprobe -
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0ffprobe version 3.2.4-1build2 Copyright (c) 2007-2017 the FFmpeg developers
  built with gcc 6.3.0 (Ubuntu 6.3.0-8ubuntu1) 20170221
  configuration: --prefix=/usr --extra-version=1build2 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --e
nable-gpl --disable-stripping --enable-avresample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libbs2b -
-enable-libcaca --enable-libcdio --enable-libebur128 --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --
enable-libgsm --enable-libmp3lame --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librubberband --enable-libshine --
enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libvpx --enable-li
bwavpack --enable-libwebp --enable-libx265 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-omx --enable-openal --enable-opengl --enable-sdl2 -
-enable-libdc1394 --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libopencv --enable-libx264 --enable-shared
  libavutil      55. 34.101 / 55. 34.101
  libavcodec     57. 64.101 / 57. 64.101
  libavformat    57. 56.101 / 57. 56.101
  libavdevice    57.  1.100 / 57.  1.100
  libavfilter     6. 65.100 /  6. 65.100
  libavresample   3.  1.  0 /  3.  1.  0
  libswscale      4.  2.100 /  4.  2.100
  libswresample   2.  3.100 /  2.  3.100
  libpostproc    54.  1.100 / 54.  1.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'pipe:':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf57.56.101
  Duration: 00:04:58.00, start: 0.000000, bitrate: N/A
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 100x56 [SAR 224:225 DAR 16:9], 13 kb/s, 25 fps, 25 tbr, 12800 tbn, 50 tbc (default
)
    Metadata:
      handler_name    : VideoHandler
```

`thumb_by_id` est une nouvelle route (Flask) en cours de construction.

## Play video with caca ASCII color output module:

```bash
┏ ↵ INT(-2)|0    latty@latty-G551JX   ~/Devel/illu…atus/illuminatus    hmx                            1.12   1.91G    96%   20:32:15  
╰─ curl http://localhost:5555/thumb_by_id/221 | cvlc - -V caca  --avcodec-hw none
```

- https://bugs.launchpad.net/ubuntu/+source/mesa/+bug/1574354
- https://mpv.io/manual/master/

# ASCIINEMA: ScreenCast

[![asciicast](https://asciinema.org/a/LpYf5QHH3op2AJR084IrThjQq.png)](https://asciinema.org/a/LpYf5QHH3op2AJR084IrThjQq)

TODO: à refaire :p

# DOCS/URLS


- https://www.google.fr/search?client=ubuntu&hs=ODz&channel=fs&dcr=0&q=python+Tools+for+managing++videos&oq=python+Tools+for+managing++videos&gs_l=psy-ab.3...4858.4858.0.4989.1.1.0.0.0.0.90.90.1.1.0....0...1..64.psy-ab..0.0.0....0.ynapQcqfVnM
- https://pypi.python.org/pypi/illuminatus/0.0.1
- https://github.com/lmjohns3/illuminatus
- => https://github.com/yoyonel/illuminatus
- http://bottlepy.org/docs/dev/
- http://click.pocoo.org/5/
- http://click.pocoo.org/5/quickstart/#screencast-and-examples
- http://flask.pocoo.org/docs/0.12/config/
- https://www.google.fr/search?client=ubuntu&hs=iaK&channel=fs&dcr=0&q=pythoncharm+debug+python+package&oq=pythoncharm+debug+python+package&gs_l=psy-ab.3...7765.8489.0.8614.5.2.0.0.0.0.0.0..0.0....0...1.1.64.psy-ab..5.0.0....0.au19vp1FKpI
- https://stackoverflow.com/questions/82875/how-to-list-the-tables-in-an-sqlite-database-file-that-was-opened-with-attach