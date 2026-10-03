# CLAUDE.md

## Project

`1panel-skills` is an Apache-2.0 collection of 8 original Agent Skills for bounded 1Panel operations. Source package version: 0.1.0, GitHub source publication; tagged release pending. It does not bundle or start an MCP server. Official 1Panel and mcp-1panel remain separate GPL-3.0 projects.

## Skill ownership

| Skill | Responsibility |
|---|---|
| 1panel-use | Discover target/capabilities and route to specialists |
| 1panel-setup | Trusted connection setup and bounded diagnosis |
| 1panel-system | Read-only system/dashboard inspection |
| 1panel-websites | Site inventory and authorized static/proxy creation |
| 1panel-certificates | SSL inventory and authorized issuance with verified accounts |
| 1panel-databases | Supported database inventory/creation and exposure limits |
| 1panel-apps | App inventory and authorized MySQL/OpenResty installation |
| 1panel-security-audit | Evidence-limited read-only security review |

## Package structure

Each skills/<name>/ contains SKILL.md, LICENSE.txt, agents/openai.yaml and local references. Agents load detailed references progressively. Standalone skills must not require sibling resources. The .claude-plugin/plugin.json skills array is the inventory source; upstream.lock.json records inspected external provenance. English client display names remain stable across languages.

## Change and verification

Follow AGENTS.md. Add meaningful failure/relocation cases to tests/ when changing discovery or required resources. Maintain both README catalogs and relevant bilingual docs. Do not copy design-skills' Harness CI jobs, OpenSpec configuration or local slash commands: this package does not implement those runtimes.

```bash
python scripts/lint_skills.py
python scripts/check_distribution.py
python -m unittest discover -s tests -v
```

Before publication, run check_distribution.py --tracked in this exact Git repository, release an immutable source version, and refresh 1panel-plugin's lock. Do not treat a local base commit or directory as an already published release.
