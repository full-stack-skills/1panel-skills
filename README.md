# 1Panel Skills

Source repository: [full-stack-skills/1panel-skills](https://github.com/full-stack-skills/1panel-skills).

Eight reusable Agent Skills for inspecting and operating an existing 1Panel server through its official MCP. This is a community skill source package with explicit capability limits and confidential credential handling.

English | [简体中文](README.zh-CN.md) · [Usage](docs/usage.md) · [Architecture](docs/1Panel-Skills-Architecture.md) · [Contributing](CONTRIBUTING.md)

## At a glance

| Item | Value |
|---|---|
| Package | `1panel-skills`, 8 registered skills |
| Version/status | 0.1.0, source on GitHub; tagged release pending |
| Skill format | SKILL.md with name, trigger description and license |
| Optional Codex metadata | agents/openai.yaml, English display names |
| Inspected MCP | v1.0.0, commit `a12b2d4ddae90f6b210b73b89ba2bc4b572dcd0c` |
| Package checks | Python 3.11+, standard library only |

## Architecture and boundary

```mermaid
flowchart LR
    U[User's bounded task] --> R[1panel-use: target and route]
    R --> S[Specialist SKILL.md]
    S --> C[Local capability and operation references]
    C --> M[User-configured official MCP connection]
    M --> P[Existing 1Panel API]
    P --> E[Observed result and read-back verification]
```

No MCP server is bundled. Each skill contains its own operational contract and capability reference. `1panel-setup` documents plugin-specific helpers as optional; standalone clients must provide their own trusted MCP connection. The separate 1panel-plugin owns standard MCP configuration and transport policy. This package does not install the panel, supply credentials, implement authentication or create an operations ledger.

The pinned MCP supports system/dashboard reads, site/SSL/app/database lists, three create operations and two app installations. Backup/restore, deletion, firewall, SSH, arbitrary SQL, generic app installation, certificate renewal and binding are outside these tools. Tool visibility is separate from operation authorization; inventories are limited to the first 500 items. Missing observations remain unknown.

## Get started from local source

Run from this package root:

```bash
python scripts/lint_skills.py
python scripts/check_distribution.py
python -m unittest discover -s tests -v
```

Expected: 8 valid skills, matching manifest and bilingual catalogs, resolvable resources and passing relocation/failure tests. These commands do not connect to a panel or install anything.

To load manually, copy the entire selected skills/<name> directory into the skill directory your Agent documents, preserving references, license and metadata. Codex user skills use `~/.agents/skills`; Claude Code project skills use `.claude/skills`. These are manual layouts, not a claim that installation was performed or tested in every client. Review existing same-name skills before replacement. Hosted installation will be documented after an actual release; no unpublished remote command is advertised.

After configuring a trusted existing MCP connection, ask:

```text
Use 1panel-system to inspect my selected panel without changes.
Separate observed facts, unknown checks and tool failures.
```

## Skill catalog

- `1panel-use`: Route 1Panel management requests to connection setup, read-only inspection, website, certificate, database, application or scoped security skills using the actual available MCP tools.
- `1panel-setup`: Set up or diagnose a 1Panel MCP connection using a pinned official executable and private plugin data; use for authentication, missing tools, transport and configuration problems.
- `1panel-system`: Inspect 1Panel system and dashboard information without mutations; use for host identity, resource observations, application counts and bounded health diagnosis.
- `1panel-websites`: Inspect or create bounded static and reverse-proxy websites through 1Panel MCP; use for site inventory and explicitly authorized site creation, preserving existing resources.
- `1panel-certificates`: Inspect 1Panel SSL certificates or request issuance through an existing ACME and DNS configuration; use for certificate inventory and explicitly authorized creation, not renewal or binding.
- `1panel-databases`: Inspect supported 1Panel database instances and create specifically authorized MySQL or PostgreSQL databases; use with explicit instance identities, exposure awareness and private credential handling.
- `1panel-apps`: Inspect installed 1Panel apps or explicitly install MySQL/OpenResty using the pinned official MCP; use with confirmed names, supported versions, ports and credential handling.
- `1panel-security-audit`: Perform a bounded read-only 1Panel risk review from available system, site, certificate and app evidence; use for prioritizing observed issues while marking firewall, SSH, WAF and backup checks unverified.

License: Apache-2.0 for original skill text. Upstream 1Panel / mcp-1panel remain GPL-3.0; their source/binaries are not redistributed here. No affiliation or official endorsement is claimed.

## Configuration and compatibility

`.claude-plugin/plugin.json` registers the source inventory. `upstream.lock.json` identifies inspected external provenance, not a binary checksum or installation proof. Each optional `agents/openai.yaml` contains an English display name and explicit invocation prompt. No API keys belong in these files.

Agents with compatible Agent Skills loading can read these skills. Codex metadata and Claude package metadata are included; actual client loading is separately verified. Cursor/OpenCode/Gemini use depends on their configured discovery, not repository presence. See [usage/configuration](docs/usage.md) for private credentials, failures and examples.

## Maintenance and verification

```text
1panel-skills/
  .claude-plugin/plugin.json   source inventory
  .github/workflows/          Windows/Linux checks
  skills/<name>/             skill + local references + metadata + license
  scripts/                   lint and distribution checks
  tests/                     relocation and missing-resource regressions
  docs/                      English/Chinese usage and architecture
  upstream.lock.json         inspected official source identity
```

Update source skills first, then deliberately refresh the plugin snapshot and file hashes. Before publication, `python scripts/check_distribution.py --tracked` requires distributed resources to be tracked in this exact Git repository. A dirty snapshot is not an immutable release. No OpenSpec/Spec Kit initialization or Harness workflow is required to maintain these instructions.

Structural validation does not prove model compliance, a production panel integration or client installation. The plugin repository owns real official-MCP tests against a loopback simulated API. See [CHANGELOG](CHANGELOG.md), [AGENTS](AGENTS.md), [CLAUDE](CLAUDE.md), [security](SECURITY.md), [contribution](CONTRIBUTING.md), [source notices](THIRD-PARTY-NOTICES.md) and [LICENSE](LICENSE).
