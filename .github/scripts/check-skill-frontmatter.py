#!/usr/bin/env python3
"""Parse every skills/*/SKILL.md frontmatter strictly, as committed at a git revision.

Strict YAML parsers (the skills CLI, Codex) silently skip a skill whose frontmatter
fails to parse, or whose description is over 1024 characters (Codex rejects it), so
a bad description must fail the build, and should stop a push before it gets there.

    check-skill-frontmatter.py [<revision>]    # default HEAD; needs PyYAML
"""
import subprocess
import sys

import yaml

LIMIT = 1024


def git(*args):
    return subprocess.run(['git', *args], check=True, capture_output=True, text=True).stdout


rev = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
paths = [p for p in git('ls-tree', '-r', '--name-only', rev, 'skills/').splitlines()
         if p.count('/') == 2 and p.endswith('/SKILL.md')]
bad = []
for path in paths:
    text = git('show', f'{rev}:{path}')
    if not text.startswith('---\n'):
        bad.append(f'{path}: no frontmatter')
        continue
    try:
        meta = yaml.safe_load(text.split('\n---', 1)[0][4:])
    except yaml.YAMLError as error:
        bad.append(f'{path}: {str(error).splitlines()[0]}')
        continue
    if not isinstance(meta, dict):
        bad.append(f'{path}: frontmatter is not a mapping')
    elif meta.get('name') != path.split('/')[1]:
        bad.append(f'{path}: name does not match its directory')
    elif not meta.get('description'):
        bad.append(f'{path}: missing description')
    elif len(str(meta['description'])) > LIMIT:
        bad.append(f"{path}: description is {len(str(meta['description']))} characters, over {LIMIT}")
print('\n'.join(bad) or f'{len(paths)} skills OK')
sys.exit(1 if bad else 0)
