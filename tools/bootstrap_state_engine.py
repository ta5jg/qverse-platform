from pathlib import Path
import re
import ast
import json
import textwrap

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / 'installer' / 'core' / 'state'
LEGACY_STATE = ROOT / 'installer' / 'core' / 'state.py'
TEST_DIR = ROOT / 'tests' / 'state'
POLICY_DIR = ROOT / 'machine' / 'policies'
REPORT_FILE = ROOT / 'state_engine_refactor_report.json'

FILES = {
    'models.py': '"""State Engine Models"""\n\n',
    'discovery.py': '"""Discovery Engine"""\n\n',
    'analysis.py': '"""Analysis Engine"""\n\n',
    'risk.py': '"""Risk Engine"""\n\n',
    'compliance.py': '"""Compliance Engine"""\n\n',
    'capacity.py': '"""Capacity Engine"""\n\n',
    'planning.py': '"""Planning Engine"""\n\n',
    'deployment.py': '"""Deployment Engine"""\n\n',
    'security.py': '"""Security Engine"""\n\n',
    'telemetry.py': '"""Telemetry Engine"""\n\n',
    'history.py': '"""History Engine"""\n\n',
    'snapshot.py': '"""Snapshot Builder"""\n\n',
    'manager.py': '"""StateManager Orchestration Layer"""\n\nfrom .discovery import *\nfrom .analysis import *\nfrom .risk import *\nfrom .compliance import *\nfrom .capacity import *\nfrom .planning import *\nfrom .deployment import *\nfrom .security import *\nfrom .telemetry import *\nfrom .history import *\nfrom .snapshot import *\n\n\nclass StateManager:\n    pass\n\n',
    '__init__.py': 'from .manager import StateManager\n\n__all__ = ["StateManager"]\n',
    'imports.py': '"""Import Resolver"""\n\n',
    'dependencies.py': '"""Dependency Resolver"""\n\n',
    'policies.py': '"""Policy Engine"""\n\n',
    'provider.py': '"""Provider Readiness Engine"""\n\n',
    'backup.py': '"""Backup Readiness Engine"""\n\n',
}


def ensure_structure():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    POLICY_DIR.mkdir(parents=True, exist_ok=True)


class StateRefactorEngine:
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.content = state_file.read_text(encoding='utf-8') if state_file.exists() else ''
        self.tree = ast.parse(self.content) if self.content else None
        self.report = {
            'dataclasses': 0,
            'functions': {},
            'unclassified': [],
            'generated_files': [],
            'coverage_percent': 0,
            'manager_warnings': [],
            'module_counts': {},
        }
    def reset_module(self, filename, header=''):
        target = STATE_DIR / filename
        target.write_text(header, encoding='utf-8')
        self.report['generated_files'].append(str(target))

    def initialize_modules(self):
        for filename, content in FILES.items():
            self.reset_module(filename, content)

    def source_segment(self, node):
        try:
            return ast.get_source_segment(self.content, node)
        except Exception:
            return None

    def extract_dataclasses(self):
        blocks = []

        if not self.tree:
            return blocks

        for node in self.tree.body:
            if isinstance(node, ast.ClassDef):
                for deco in node.decorator_list:
                    if isinstance(deco, ast.Name) and deco.id == 'dataclass':
                        src = self.source_segment(node)
                        if src:
                            blocks.append('@dataclass\n' + src)
                        break

        return blocks

    def extract_functions_by_prefix(self, prefixes):
        blocks = []

        if not self.tree:
            return blocks

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if any(node.name.startswith(p) for p in prefixes):
                    src = self.source_segment(node)
                    if src:
                        blocks.append(src)

        return blocks

    def classify_function(self, node):
        name = node.name

        rules = {
            'discovery': [
                'command_exists', 'get_version', 'service_running', 'detect', 'detect_'
            ],
            'analysis': [
                'analyze', 'analyze_', 'score_', 'recommend_', 'build_environment_profile'
            ],
            'risk': [
                'assess_', 'dependency_', 'build_dependency_graph'
            ],
            'compliance': [
                'evaluate_compliance', 'evaluate_policies'
            ],
            'capacity': [
                'calculate_', 'estimate_', 'benchmark_'
            ],
            'planning': [
                'build_installation_', 'build_repair_', 'build_executive_summary'
            ],
            'deployment': [
                'evaluate_deployment_'
            ],
            'security': [
                'evaluate_security_'
            ],
            'telemetry': [
                'build_telemetry'
            ],
            'history': [
                'save_history_', 'latest_snapshot', 'diff_against_', 'save', 'load'
            ],
            'snapshot': [
                'generate_snapshot'
            ],
            'provider': [
                'evaluate_ai_readiness', 'evaluate_provider_readiness'
            ],
            'backup': [
                'evaluate_backup_readiness'
            ],
        }

        for module, prefixes in rules.items():
            if any(name.startswith(p) for p in prefixes):
                return module

        return None

    def build_models(self):
        models = self.extract_dataclasses()
        target = STATE_DIR / 'models.py'

        with target.open('a', encoding='utf-8') as f:
            for item in models:
                f.write('\n\n')
                f.write(item)

        print(f'[MODELS] {len(models)} dataclass block(s) exported')
        self.report['dataclasses'] = len(models)

    def build_discovery(self):
        functions = self.extract_functions_by_prefix(['detect_'])
        target = STATE_DIR / 'discovery.py'

        with target.open('a', encoding='utf-8') as f:
            for item in functions:
                f.write('\n\n')
                f.write(item)

        print(f'[DISCOVERY] {len(functions)} detect_* function(s) exported')

    def append_blocks(self, target_name, blocks, label):
        target = STATE_DIR / target_name

        with target.open('a', encoding='utf-8') as f:
            for item in blocks:
                f.write('\n\n')
                f.write(item)

        print(f'[{label}] {len(blocks)} block(s) exported')
        self.report['functions'][label.lower()] = len(blocks)
    def build_tests(self):
        TEST_DIR.mkdir(parents=True, exist_ok=True)

        tests = {
            'test_discovery.py': 'def test_discovery_placeholder():\n    assert True\n',
            'test_analysis.py': 'def test_analysis_placeholder():\n    assert True\n',
            'test_compliance.py': 'def test_compliance_placeholder():\n    assert True\n',
            'test_planning.py': 'def test_planning_placeholder():\n    assert True\n',
        }

        for name, content in tests.items():
            path = TEST_DIR / name
            if not path.exists():
                path.write_text(content, encoding='utf-8')

    def build_policy_files(self):
        POLICY_DIR.mkdir(parents=True, exist_ok=True)

        defaults = {
            'production.yaml': 'ssl_required: true\nbackup_required: true\nfirewall_required: true\n',
            'staging.yaml': 'ssl_required: true\nbackup_required: true\n',
            'development.yaml': 'ssl_required: false\nbackup_required: false\n',
        }

        for name, content in defaults.items():
            target = POLICY_DIR / name
            if not target.exists():
                target.write_text(content, encoding='utf-8')

    def calculate_coverage(self):
        total = 0
        classified = 0

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                total += 1
                if self.classify_function(node):
                    classified += 1
                elif not node.name.startswith('__'):
                    self.report['unclassified'].append(node.name)

        self.report['coverage_percent'] = (
            round((classified / total) * 100, 2)
            if total else 100
        )

    def build_analysis(self):
        blocks = self.extract_functions_by_prefix(
            ['analyze_', 'score_', 'recommend_']
        )
        self.append_blocks('analysis.py', blocks, 'ANALYSIS')

    def build_risk(self):
        blocks = self.extract_functions_by_prefix(
            ['assess_', 'dependency_']
        )
        self.append_blocks('risk.py', blocks, 'RISK')

    def build_compliance(self):
        blocks = self.extract_functions_by_prefix(
            ['evaluate_']
        )
        self.append_blocks('compliance.py', blocks, 'COMPLIANCE')

    def build_capacity(self):
        blocks = self.extract_functions_by_prefix(
            ['calculate_', 'estimate_', 'benchmark_']
        )
        self.append_blocks('capacity.py', blocks, 'CAPACITY')

    def build_planning(self):
        blocks = self.extract_functions_by_prefix(
            ['build_installation_', 'build_repair_']
        )
        self.append_blocks('planning.py', blocks, 'PLANNING')

    def build_deployment(self):
        blocks = self.extract_functions_by_prefix(
            ['evaluate_deployment_']
        )
        self.append_blocks('deployment.py', blocks, 'DEPLOYMENT')

    def build_security(self):
        blocks = self.extract_functions_by_prefix(
            ['evaluate_security_']
        )
        self.append_blocks('security.py', blocks, 'SECURITY')

    def build_telemetry(self):
        blocks = self.extract_functions_by_prefix(
            ['build_telemetry']
        )
        self.append_blocks('telemetry.py', blocks, 'TELEMETRY')

    def build_history(self):
        blocks = self.extract_functions_by_prefix(
            ['save_history_', 'latest_snapshot', 'diff_against_']
        )
        self.append_blocks('history.py', blocks, 'HISTORY')


    def build_snapshot(self):
        blocks = self.extract_functions_by_prefix(['generate_snapshot'])
        self.append_blocks('snapshot.py', blocks, 'SNAPSHOT')


    def build_provider(self):
        blocks = self.extract_functions_by_prefix([
            'evaluate_ai_readiness',
            'evaluate_provider_readiness'
        ])
        self.append_blocks('provider.py', blocks, 'PROVIDER')


    def build_backup(self):
        blocks = self.extract_functions_by_prefix([
            'evaluate_backup_readiness'
        ])
        self.append_blocks('backup.py', blocks, 'BACKUP')

    def build_import_resolver(self):
        target = STATE_DIR / 'imports.py'

        target.write_text(
            '"""Import Resolver"""\n\n# Generated by State Engine Bootstrap V6\n',
            encoding='utf-8',
        )

        print('[IMPORTS] imports.py generated')

    def build_dependency_resolver(self):
        target = STATE_DIR / 'dependencies.py'

        target.write_text(
            '"""Dependency Resolver"""\n\n# Generated by State Engine Bootstrap V6\n',
            encoding='utf-8',
        )

        print('[DEPENDENCIES] dependencies.py generated')

    def build_policy_engine(self):
        target = STATE_DIR / 'policies.py'

        target.write_text(
            '"""Policy Engine"""\n\n# YAML policy loading will live here\n',
            encoding='utf-8',
        )

        print('[POLICIES] policies.py generated')

    def build_manager(self):
        target = STATE_DIR / 'manager.py'

        manager_code = '''"""StateManager Orchestration Layer"""

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
'''

        target.write_text(manager_code, encoding='utf-8')

        print('[MANAGER] manager.py generated')

    def validate_generated_modules(self):
        expected = [
            'models.py',
            'discovery.py',
            'analysis.py',
            'risk.py',
            'compliance.py',
            'capacity.py',
            'planning.py',
            'deployment.py',
            'security.py',
            'telemetry.py',
            'history.py',
            'provider.py',
            'backup.py',
            'snapshot.py',
            'manager.py',
        ]

        for name in expected:
            target = STATE_DIR / name
            if not target.exists():
                self.report['manager_warnings'].append(
                    f'missing_module:{name}'
                )

    def save_report(self):
        self.report['module_counts'] = self.report['functions']
        REPORT_FILE.write_text(
            json.dumps(self.report, indent=2),
            encoding='utf-8',
        )

    def run(self):
        if not self.state_file.exists():
            print('[WARN] legacy state.py not found')
            return

        self.initialize_modules()

        self.build_models()
        self.build_discovery()
        self.build_analysis()
        self.build_risk()
        self.build_compliance()
        self.build_capacity()
        self.build_planning()
        self.build_deployment()
        self.build_security()
        self.build_telemetry()
        self.build_history()
        self.build_snapshot()
        self.build_provider()
        self.build_backup()
        self.build_import_resolver()
        self.build_dependency_resolver()
        self.build_policy_engine()
        self.build_manager()

        self.build_tests()
        self.build_policy_files()

        self.calculate_coverage()
        self.validate_generated_modules()
        self.save_report()

        print('[DONE] State Engine V9 architecture bootstrap complete')


if __name__ == '__main__':
    ensure_structure()

    engine = StateRefactorEngine(LEGACY_STATE)
    engine.run()

    print('\nState Engine V9 bootstrap complete.')