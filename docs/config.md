# Configuring Addok

By default, Addok is configured for a French database of addresses from France
*(It may be because it has been initially coded in Paris… ;) )*

But certainly your needs are different, and even if you deal with French addresses
you may want to define **which fields are indexed** or **which filters are
available** for example.

## Registering your custom config file

An Addok config file is simply a python file that define some keys. This file
needs to be in your pythonpath, and you need to define an environment variable
that points to it:

    export ADDOK_CONFIG_MODULE=path.to.my.config

## Environment settings

Some settings are used to define how addok will deal with the system it's
installed on.

#### DB (dict)
Defines the Redis database settings:

    DB = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }

#### LOG_DIR (path)
Path to the directory Addok will write its log and history files. Can also
be overriden from the environment variable `ADDOK_LOG_DIR`.

    LOG_DIR = 'path/to/dir'


## Basic settings

A bunch of settings you may want to change to fit your custom instance.

#### ATTRIBUTION (string or dict)
The attribution of the data that will be used in the API results. Can be a
simple string, or a dict `{source: attribution, source2: attribution2}`.

    ATTRIBUTION = 'OpenStreetMap Contributors'

#### FIELDS (list of dict)
The document fields you want to index. It's a list of dict, each one defining
an indexed field. Available keys:

- **key** (*mandatory*): the key of the field in the document
- **boost**: optional boost of the field (default: 1)
- **null**: define if the field can be null (default: True)

```
FIELDS = [
    {'key': 'name', 'boost': 4, 'null': False},
    {'key': 'street'},
    {'key': 'postcode',
     'boost': lambda doc: 1.2 if doc.get('type') == 'commune' else 1},
    {'key': 'city'},
    {'key': 'housenumbers'}
]
```

#### FILTERS (list)
A list of fields to be indexed as available filters. Keep in mind that every
filter means bigger index.

    FILTERS = ["type", "postcode"]

#### LICENCE (string or dict)
The licence of the data returned by the API. Can be a simple string, or a dict
`{source: licence, source2: licence2}`.

    LICENCE = "ODbL"

#### PROCESSORS (iterable of python paths)
Define the various functions to preprocess the text, before indexing and
searching. It's an `iterable` of python paths. Some functions are built in
(mainly for French at this time, but you can point to any python function that
is on the pythonpath).

    PROCESSORS = [
        'addok.textutils.default.pipeline.tokenize',
        'addok.textutils.default.pipeline.normalize',
        'addok.textutils.default.pipeline.synonymize',
        'addok.textutils.fr.phonemicize',
    ]

#### QUERY_PROCESSORS (iterable of python paths)
Additional processors that are run only at query time.

    QUERY_PROCESSORS = (
        'addok.textutils.fr.extract_address',
        'addok.textutils.fr.clean_query',
        'addok.textutils.fr.glue_ordinal',
    )

#### SYNONYMS_PATH (path)
Path to the synonym file. Synonyms file are in the format `av, ave => avenue`.

    SYNONYMS_PATH = RESOURCES_ROOT.joinpath('synonyms').joinpath('fr.txt')

## Advanced settings

Those are internal settings. Change them with caution.

#### BUCKET_LIMIT (int)
The max number of items addok will try to fetch from Redis before scoring and
sorting them. Note that **this is not the number of returned results**.

    BUCKET_LIMIT = 1000

#### COMMON_THRESHOLD (int)
Above this treshold, terms are considered commons, and thus with less importance
in the search algorithm.

    COMMON_THRESHOLD = 10000

#### DEFAULT_BOOST (float)
Default score for the relation token to document.

    DEFAULT_BOOST = 1.0

#### GEOHASH_PRECISION (int)
Size of the geohash. The bigger the setting, the smaller the hash.
See [Geohash on Wikipedia](http://en.wikipedia.org/wiki/Geohash).

    GEOHASH_PRECISION = 8

#### IMPORTANCE_WEIGHT (float)
The max inherent score of a document in the final score.

    IMPORTANCE_WEIGHT = 0.1

#### INTERSECT_LIMIT (int)
Above this treshold, we avoid intersecting sets.

    INTERSECT_LIMIT = 100000

#### MATCH_THRESHOLD (float between 0 and 1)
Min score used to consider a result may *match* the query.

    MATCH_THRESHOLD = 0.9

## Nominatim settings

#### NOMINATIM_CREDENTIALS (dict)
Credential for connecting to Nominatim database

    NOMINATIM_CREDENTIALS = {
        'dbname': 'nominatim'
    }

#### NOMINATIM_ITERSIZE (int)
Size of the connection cursor.

    NOMINATIM_ITERSIZE = 1000

#### NOMINATIM_LIMIT (int)
Optional limit when querying Nominatim.

    NOMINATIM_LIMIT = None

#### NOMINATIM_PROCESSORS (iterable)
Iterable of module to preprocess Nominatim data.

    NOMINATIM_PROCESSORS = (
        'addok.batch.nominatim.query',
        'addok.batch.nominatim.get_context',
        'addok.batch.nominatim.get_housenumbers',
        'addok.batch.nominatim.row_to_doc',
    )

#### NOMINATIM_MODE (string)
Nominatim import mode, one of `full`, `noaddress`, `onlyaddress`.

    NOMINATIM_MODE = 'full'