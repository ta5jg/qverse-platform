#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

PLACEHOLDER_MARKERS = (
    'todo',
)

PLACEHOLDER_EXACT_LINES = (
    '...',
)

PLACEHOLDER_SCRIPT_PREFIXES = (
    'scripts/bootstrap_',
)

IGNORED_PLACEHOLDER_FILES = (
    'scripts/audit_project.py',
    'scripts/repair_project.py',
)

IGNORED_PLACEHOLDER_FILE_NAMES = (
    'repair_project.py',
    'audit_project.py',
)

IGNORED_PLACEHOLDER_PREFIXES = (
    'deploy/',
    'docs/',
    '.qverse_installer/',
    '.qverse_backups/',
    'reports/',
)

def scan_project():
    ignore_parts = {'__pycache__', '.git', 'node_modules', 'dist', 'build', '.venv', 'venv', 'reports'}
    critical_prefixes = (
        'api/',
        'frontend/src/',
        'agent/',
        'ai/',
        'ecosystem/',
        'game/',
        'infrastructure/',
    )
    empty_files = []
    placeholder_files = []
    critical_files = []
    total_files = 0

    for filepath in ROOT.rglob('*'):
        if filepath.is_file():
            if any(part in ignore_parts for part in filepath.parts):
                continue
            total_files += 1
            try:
                content = filepath.read_text(encoding='utf-8')
            except Exception:
                continue
            rel_path = str(filepath.relative_to(ROOT)).replace('\\', '/')
            is_empty = content.strip() == ''
            is_placeholder = False
            lowered = content.lower()
            stripped_lines = [line.strip().lower() for line in content.splitlines()]
            placeholder_scan_allowed = not rel_path.startswith(IGNORED_PLACEHOLDER_PREFIXES)
            placeholder_scan_allowed = placeholder_scan_allowed and not rel_path.startswith(PLACEHOLDER_SCRIPT_PREFIXES)
            placeholder_scan_allowed = placeholder_scan_allowed and rel_path not in IGNORED_PLACEHOLDER_FILES
            placeholder_scan_allowed = placeholder_scan_allowed and filepath.name not in IGNORED_PLACEHOLDER_FILE_NAMES

            if placeholder_scan_allowed:
                if any(marker in lowered for marker in PLACEHOLDER_MARKERS):
                    is_placeholder = True
                if any(line in PLACEHOLDER_EXACT_LINES for line in stripped_lines):
                    is_placeholder = True
            if is_empty:
                empty_files.append(rel_path)
            elif is_placeholder:
                placeholder_files.append(rel_path)
            if (is_empty or is_placeholder) and any(rel_path.startswith(prefix) for prefix in critical_prefixes):
                critical_files.append(rel_path)

    return {
        'empty': empty_files,
        'placeholder': placeholder_files,
        'critical': critical_files,
        'total_files': total_files
    }

def repair_report(data):
    empty = data.get('empty', [])
    placeholder = data.get('placeholder', [])
    critical = data.get('critical', [])
    total_files = data.get('total_files', 0)
    healthy = len(empty) == 0 and len(placeholder) == 0 and len(critical) == 0
    status = 'healthy' if healthy else 'needs_repair'
    return {
        'status': status,
        'empty_count': len(empty),
        'placeholder_count': len(placeholder),
        'critical_count': len(critical),
        'total_files': total_files,
        'empty_files': empty,
        'placeholder_files': placeholder,
        'critical_files': critical
    }

def write_report(report):
    report_dir = ROOT / 'reports'
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / 'project_repair_report.json'
    with report_path.open('w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    with (report_dir / 'empty_files.txt').open('w', encoding='utf-8') as f:
        for path in report.get('empty_files', []):
            f.write(path + '\n')
    with (report_dir / 'placeholder_files.txt').open('w', encoding='utf-8') as f:
        for path in report.get('placeholder_files', []):
            f.write(path + '\n')
    with (report_dir / 'critical_files.txt').open('w', encoding='utf-8') as f:
        for path in report.get('critical_files', []):
            f.write(path + '\n')

def main():
    parser = argparse.ArgumentParser(description='Q-Verse V10.4 Repair Engine')
    parser.add_argument('--json', action='store_true', help='Output full JSON report')
    args = parser.parse_args()

    print('Q-Verse V10.4 Repair Engine Started')
    data = scan_project()
    report = repair_report(data)
    write_report(report)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"[FILES] {report['total_files']}")
        print(f"[EMPTY] {report['empty_count']}")
        print(f"[PLACEHOLDER] {report['placeholder_count']}")
        print(f"[CRITICAL] {report['critical_count']}")
        print(f"[STATUS] {report['status']}")

    print('Q-Verse V10.4 Repair Engine Complete')

if __name__ == '__main__':
    main()
