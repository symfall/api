import os

from .default import *  # noqa

DEPLOYMENT_ARCHITECTURE = os.getenv("DEPLOYMENT_ARCHITECTURE")

if DEPLOYMENT_ARCHITECTURE == "development":
    from .development import *  # noqa

elif DEPLOYMENT_ARCHITECTURE == "production":
    from .production import *  # noqa


globals().update(os.environ)
