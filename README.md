# CAM4ModelExtractor

This script finds online models on CAM4. If the a model matches a given filter,
their username is written to a file. This can be used in conjunction with scripts such as
[beaston02/CAM4Recorder](https://github.com/beaston02/CAM4Recorder) to automaticly capture
the matched cams.

## Installation

Python 3.5 or higher. Install the required python modules with pip
```bash
pip install -r requirements.txt
```

Run with
```bash
python CAM4Extractor.py
```

## Usage and initial setup

### config.config
You need to edit the config file `config.config`. The entries should be
self explanatory.

### filters.json

Filters.json sets which models are being extracted. Any regex expression
is allowed in the filter entries. Each filter has its own output file with
the given name in the output folder. The exportToCapture field sets if the
newly discovered models should be appended to [beaston02/CAM4Recorder](https://github.com/beaston02/CAM4Recorder) wishlist.


The example given bellow creates two filters. The first filter extracts
female models from the US, and exports them to the CAM4Recorder wanted list.
The second example captures bisexual models from germany, and does not export
them to the CAM4Recorder wanted list.
```json
[
  {
    "name": "female-us",
    "country": "us",
    "gender": "female",
    "orientation": ".*",
    "title": ".*",
    "url": ".*",
    "exportToCapture": true
  },
   {
    "name": "german-bisexual",
    "country": "de",
    "gender": "*",
    "orientation": "bisexual",
    "title": ".*",
    "url": ".*",
    "exportToCapture": false
  }
]
```