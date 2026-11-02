from .linkedin import LinkedIn
from .x import X
from .youtube import YouTube

REGISTRY = {
    'youtube':  YouTube,
    'x':        X,
    'linkedin': LinkedIn,
}
