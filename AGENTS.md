# 1Panel Skills maintenance

Read README.md / README.zh-CN.md and CLAUDE.md before changes. This repository owns original reusable skill text; 1panel-plugin owns the transport runtime and vendored snapshots.

- Keep skill names stable, lowercase kebab-case. Each skills/<name>/SKILL.md needs name, a single-line trigger description, and license. Include self-contained references and license files.
- Update the source skills first, then deliberately refresh the plugin snapshot and hashes. Never edit a vendored skill as its only source of truth.
- Register every distributed skill in .claude-plugin/plugin.json and both README catalogs. Maintain English client display names and consistent Chinese/English capabilities.
- Verify tool names, schema and restrictions against upstream.lock.json's pinned official source. Panel UI features are not automatically MCP tools. Do not upgrade the pin or promise unsupported operations without review and runtime tests.
- Preserve user modifications. Do not create/switch branches, initialize specification tools, install clients or change credentials without user authorization.
- No secrets in docs/configs, no automatic installation or live panel operations in CI. Real MCP integration uses a simulated panel endpoint in the plugin repository.
- Run the lint, distribution check and regression tests before completion. Publication additionally requires --tracked and a clean released source snapshot; local structure validation is not proof of publication or installation.
