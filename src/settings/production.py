from .default import *  # pylint: disable=unused-wildcard-import,wildcard-import

DEBUG = False

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
    "rest_framework.renderers.JSONRenderer",
)
