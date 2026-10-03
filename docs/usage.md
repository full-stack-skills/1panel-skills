# 1Panel Skills usage and configuration

## Choose a task, then discover capabilities

Use 1panel-use when routing is unclear. A named specialist can be invoked directly; do not route every step again. Resolve the selected panel connection, exact target and discovered tools before calls. Host-specific namespace prefixes do not change the upstream tool names. References are loaded progressively from the selected skill directory.

| Request | Skill | Observable result |
|---|---|---|
| Read-only health inspection | 1panel-system | Actual system/dashboard fields, failed or unknown checks |
| Website creation | 1panel-websites | Existing-site preflight, one bounded submission, exact-domain read-back |
| Certificate request | 1panel-certificates | Confirmed domain/provider/accounts, issuance versus active TLS separated |
| Database creation | 1panel-databases | Exact instance/type/name, exposure and credential limits, supported verification |
| Application installation | 1panel-apps | Existing apps, confirmed ports/version limits, actual task/application status |
| Risk review | 1panel-security-audit | Evidence-backed findings; unavailable firewall/SSH/backup checks unverified |

## Repository configuration

| File | Role | Secret handling |
|---|---|---|
| .claude-plugin/plugin.json | Source inventory/version/author/license | No credentials |
| upstream.lock.json | Inspected official source commit and capability provenance | No runtime token or executable identity |
| skills/*/agents/openai.yaml | English display name, description and explicit prompt | No provider authentication |
| .gitattributes / .editorconfig | Stable LF/UTF-8 authoring for source hashes | No runtime behavior |
| .github/workflows/skill-lint.yml | Windows/Linux local package checks | No real panel/key required |

The source package intentionally has no mcp.json: it does not provide an MCP server. The separate plugin has standard root mcp.json because it integrates one. Do not add empty or fictitious service declarations to a skill-only source package.

## Connection and credentials

The user must supply a trusted existing official MCP connection and enable/configure the panel API appropriately. Never ask for its key in chat. A standalone skill can guide setup but cannot assume plugin helper files exist.

With 1panel-plugin, the user/client provides its absolute private data directory. Its explicit setup helper records verified official binary path/SHA256, HTTPS panel origin, reviewed upstream commit and requested access level in connection.json, with the key in separately protected credentials.json. No visible MCP manifest contains the key; the launch boundary supplies it to the official child process environment. Those private runtime files are outside this skill package and never copied into its release.

Portable clients supply PLUGIN_DATA. Native clients that do not expand it need an explicit absolute path in their private native configuration. Do not guess HOME/APPDATA, borrow a different panel configuration, disable TLS verification or install missing prerequisites silently. Access level defaults to readonly; readwrite adds three create tools and full adds two app-install tools. A change requires MCP reconnection. Local availability is not panel-side RBAC or permission for every operation.

## Examples and important limits

Read-only example: “Use 1panel-system to inspect my selected panel and separate observations from guesses.” No subsequent installation is implied.

Bounded write example: “Create the static website for my specified domain on the selected panel.” Resolve domain/target, existing resources and dependencies first; preserve this explicit authorization. Do not ask again merely because the tool writes, but stop for a material ambiguity or unsupported requirement.

For unknown write outcomes, inspect resulting state before another submission. The pinned official list tools return at most 500 items; do not claim exhaustive inventory when capped. Certificate creation chooses the first ACME account internally, so manual account confirmation is required. MySQL database creation defaults source permission to `%`; narrow permissions cannot be expressed. Generated passwords are not a reliable delivery path. Exact OpenResty version selection and PostgreSQL inventory are not guaranteed by these tools. See the selected skill's local tools reference for complete restrictions.

## Troubleshooting

| Symptom | First action |
|---|---|
| Skill not discovered | Check supported skill root, exact directory/name and complete copied files |
| Tool missing | Inspect tools/list and configured access; do not invent the tool |
| API authentication failure | Safely check target, API enablement, source allowlist, key and clock |
| Certificate prerequisites unknown | Verify existing ACME/DNS account in the panel; no account-list MCP tool exists |
| Timeout during creation | Mark unknown, inspect actual state, no blind retry or automatic deletion |
| Structural tests pass but operations fail | Structure is not a real MCP/panel/client integration test |

Validate from README.md and keep the same skill identities in both languages. See [security](../SECURITY.md) and [architecture](1Panel-Skills-Architecture.md).
