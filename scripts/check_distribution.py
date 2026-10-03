"""Check the standalone skill package without dependencies or network access."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')
REQUIRED = ['README.md', 'README.zh-CN.md', 'LICENSE', 'AGENTS.md', 'CLAUDE.md',
            'CONTRIBUTING.md', 'SECURITY.md', 'CHANGELOG.md', 'THIRD-PARTY-NOTICES.md',
            '.gitignore', '.gitattributes', '.editorconfig', 'upstream.lock.json',
            '.github/workflows/skill-lint.yml', 'docs/usage.md', 'docs/usage.zh-CN.md',
            'docs/1Panel-Skills-Architecture.md', 'docs/1Panel-Skills-Architecture.zh_CN.md']


def validate(root):
    root = root.resolve()
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append('missing package file: ' + name)
    try:
        manifest = json.loads((root / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        expected = manifest['skills']
        actual = sorted('./skills/' + p.name for p in (root / 'skills').iterdir() if p.is_dir())
        if not isinstance(expected, list) or sorted(expected) != actual or len(set(expected)) != len(expected):
            errors.append('manifest inventory differs from skill directories')
        if manifest.get('name') != '1panel-skills' or not re.fullmatch(r'\d+\.\d+\.\d+', manifest.get('version', '')):
            errors.append('package identity/version is invalid')
        if manifest.get('license') != 'Apache-2.0' or not isinstance(manifest.get('author'), dict):
            errors.append('package license/author metadata is missing')
        provenance = json.loads((root / 'upstream.lock.json').read_text(encoding='utf-8'))
        if provenance.get('commit') != 'a12b2d4ddae90f6b210b73b89ba2bc4b572dcd0c' or provenance.get('ref') != 'v1.0.0':
            errors.append('reviewed upstream identity drifted; revalidate capabilities')
    except (OSError, ValueError, KeyError, TypeError):
        return errors + ['package manifest or provenance is invalid']
    for relative in actual:
        skill = root / relative[2:]
        for name in ['SKILL.md', 'LICENSE.txt', 'references/tools.md', 'references/operation-contract.md', 'agents/openai.yaml']:
            if not (skill / name).is_file():
                errors.append(f'{skill.name}: missing {name}')
        for readme in ['README.md', 'README.zh-CN.md']:
            if (root / readme).is_file() and skill.name not in (root / readme).read_text(encoding='utf-8'):
                errors.append(f'{readme}: missing skill {skill.name}')
        metadata = skill / 'agents/openai.yaml'
        if metadata.is_file():
            text = metadata.read_text(encoding='utf-8')
            fields = dict(re.findall(r'^  (display_name|short_description|default_prompt): "([^"]*)"$', text, re.M))
            if set(fields) != {'display_name', 'short_description', 'default_prompt'}:
                errors.append(f'{skill.name}: client metadata must use quoted string fields')
            elif (not fields['display_name'].isascii() or not 25 <= len(fields['short_description']) <= 64
                  or '$' + skill.name not in fields['default_prompt']):
                errors.append(f'{skill.name}: invalid English metadata or explicit prompt')
    for markdown in root.rglob('*.md'):
        if any(part in {'.git', '__pycache__', 'node_modules'} for part in markdown.parts):
            continue
        text = markdown.read_text(encoding='utf-8')
        fence = False
        for number, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith('```'):
                fence = not fence
                continue
            if fence:
                continue
            for match in LINK.finditer(line):
                target = unquote(match[1].strip().strip('<>').split('#', 1)[0])
                if not target or re.match(r'^[a-z]+://|^mailto:', target):
                    continue
                path = (markdown.parent / target).resolve()
                if root != path and root not in path.parents or not path.exists():
                    errors.append(f'{markdown.relative_to(root)}:{number}: invalid local link {target}')
        if fence:
            errors.append(f'{markdown.relative_to(root)}: unclosed code fence')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--tracked', action='store_true', help='Require resources tracked in this exact Git repository before publication')
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate(root)
    if args.tracked:
        try:
            repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()).resolve()
            if repo != root:
                raise ValueError()
            tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0'))
            for file in root.rglob('*'):
                if file.is_file() and not any(part in {'.git', '__pycache__', 'node_modules', 'dist'} for part in file.relative_to(root).parts) and file.suffix != '.pyc':
                    if file.relative_to(root).as_posix() not in tracked:
                        errors.append('untracked distributed resource: ' + file.relative_to(root).as_posix())
        except (OSError, ValueError, subprocess.SubprocessError):
            errors.append('--tracked requires this package to be its own Git repository')
    count = sum(p.is_dir() for p in (root / 'skills').iterdir())
    print(json.dumps({'valid': not errors, 'skills': count, 'tracked_check': args.tracked, 'errors': errors}, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
