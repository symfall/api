from .default import *  # noqa

DEBUG = False

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (  # noqa
    "rest_framework.renderers.JSONRenderer",
)
