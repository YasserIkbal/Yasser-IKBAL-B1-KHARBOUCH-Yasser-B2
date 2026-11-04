"""Compatibilité historique : préférer ``sentiment_app.predict``.

Le module est un alias du nouveau module afin que les anciens tests qui
modifient ``src.predict.MODELE`` continuent de modifier la même configuration.
"""

import sys

from sentiment_app import predict as _implementation

sys.modules[__name__] = _implementation
