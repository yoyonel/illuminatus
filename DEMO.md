# Installation

```bash
mkvirtualenv --python=/usr/bin/python3 py3_illuminatus
pip freeze
pip install -r requirements.txt
pip freeze
python setup.py install 
pip freeze
```

# Base pré-existante

https://stackoverflow.com/questions/11753871/getting-the-type-of-a-column-in-sqlite

```bash
du -sh db
tree du
```

```bash
sqlite3 db/db.sql3
sqlite> .table
sqlite> PRAGMA table_info(media);
sqlite> SELECT id, path, medium, stamp FROM media LIMIT 5;
sqlite> SELECT id, meta FROM media LIMIT 1;
```

# Import dans la base

```bash
PYTHONPATH=. illuminatus --db db/db.sql3 \
	--video-format '100,acodec=' \
	import "/home/latty/Devel/screenpulse-tests/datas/sp-back02/2002/extract_2002_20170802_103*.mp4" \
	--tag 2002 --tag sp-back02
```

# Listings

```bash
PYTHONPATH=. illuminatus --db db/db.sql3 ls "sp-back02 & after:2017-08-02T10:30:00.00 & before:2017-08-02T10:40:00.00"
PYTHONPATH=. illuminatus --db db/db.sql3 ls "sp-back02 & after:2017-08-02T10:30:00.00 & before:2017-08-02T10:40:00.00" --order tag
PYTHONPATH=. illuminatus --db db/db.sql3 ls "2002 & sp-back02 & after:2017-08-02T10:30:00.00 & before:2017-08-02T10:40:00.00" --order tag
```

# Delete

```bash
PYTHONPATH=. illuminatus --db db/db.sql3 rm "2002 & sp-back02 & after:2017-08-02T10:30:00.00 & before:2017-08-02T10:40:00.00"
PYTHONPATH=. illuminatus --db db/db.sql3 ls "2002 & sp-back02 & after:2017-08-02T10:30:00.00 & before:2017-08-02T10:40:00.00" --order tag

PYTHONPATH=. illuminatus --db db/db.sql3 \
	--video-format '100,acodec=' \
	import "/home/latty/Devel/screenpulse-tests/datas/sp-back02/2002/extract_2002_20170802_103*.mp4" \
	--tag 2002 --tag sp-back02
```

# Serve

```bash
PYTHONPATH=. illuminatus --db db/db.sql3 serve
```

## Request

https://stackoverflow.com/questions/7373752/how-do-i-get-curl-to-not-show-the-progress-bar
https://stackoverflow.com/questions/31827012/python-importing-urllib-quote
https://stackoverflow.com/questions/16908236/how-to-execute-python-inline-from-a-bash-shell

### Results by filters

```bash
curl -s http://localhost:5555/query/$(python -c "import urllib.parse; print(urllib.parse.quote('2002 & after:2017-08-02T10:30:00.00 & before:2017-08-02T10:40:00.00'))") | grep "\"id\""
	"id": 409, 
    "id": 410,
```

### Retrieve Thumb from id

```bash
curl -s http://localhost:5555/thumb_by_id/409 | ffprobe -
```