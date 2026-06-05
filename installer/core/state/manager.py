"""StateManager Orchestration Layer"""

from .discovery import *
from .analysis import *
from .risk import *
from .compliance import *
from .capacity import *
from .planning import *
from .deployment import *
from .security import *
from .telemetry import *
from .history import *
from .snapshot import *
from .provider import *
from .backup import *
from .imports import *
from .dependencies import *
from .policies import *


class StateManager:
    """Main orchestration facade for the modular State Engine."""

    MODULES = [
        'discovery',
        'analysis',
        'risk',
        'compliance',
        'capacity',
        'planning',
        'deployment',
        'security',
        'telemetry',
        'history',
        'provider',
        'backup',
        'snapshot',
    ]

    def generate_snapshot(self):
        raise NotImplementedError('Generated facade - implementation will be migrated from legacy state.py')
