# 1Panel Skills

源码仓库：[full-stack-skills/1panel-skills](https://github.com/full-stack-skills/1panel-skills)。

面向既有 1Panel 服务器的 8 个可复用 Agent Skills，通过官方 MCP 执行有明确范围的检查与操作。本包为社区维护的技能源码，明确区分实际能力、授权和验证证据。

[English](README.md) | 简体中文 · [使用说明](docs/usage.zh-CN.md) · [架构](docs/1Panel-Skills-Architecture.zh_CN.md) · [贡献](CONTRIBUTING.md)

## 一眼看懂

| 属性 | 当前事实 |
|---|---|
| 技能包 | `1panel-skills`，8 个已登记技能 |
| 版本与状态 | 0.1.1，源码托管于 GitHub，固定版本 v0.1.1 |
| 技能格式 | SKILL.md，包含名称、触发描述和许可证 |
| Codex 可选配置 | agents/openai.yaml，统一英文显示名称 |
| 已检查的官方 MCP | v1.0.0，commit `a12b2d4ddae90f6b210b73b89ba2bc4b572dcd0c` |
| 本地检查环境 | Python 3.11+，仅使用标准库 |

## 架构与边界

```mermaid
flowchart LR
    U[用户有明确范围的任务] --> R[1panel-use：确认目标并分流]
    R --> S[专业技能 SKILL.md]
    S --> C[技能内部能力与操作合同]
    C --> M[用户已配置的官方 MCP 连接]
    M --> P[既有 1Panel API]
    P --> E[实际结果与只读复核]
```

本包提供技能说明、内部引用和客户端元数据，不包含或启动 MCP 服务，不安装面板，不提供密钥，不实现认证，也不另建运维账本。配套 1panel-plugin 负责标准 MCP 配置和运行时权限控制；技能也能独立配合可信的已有连接使用。1panel-setup 中的插件辅助脚本属于可选指引，不伪称本技能源仓库包含这些脚本。

锁定的 MCP 支持系统和仪表盘读取、网站/证书/应用/数据库列表、三类创建及两类应用安装。备份恢复、删除、防火墙、SSH、任意 SQL、通用应用安装、证书续期与绑定不在工具范围内。工具可见不等于已授权执行。上游列表最多返回首页 500 条，缺失观察必须标为未知。

## 从本地源码开始

在包根目录执行：

```bash
python scripts/lint_skills.py
python scripts/check_distribution.py
python -m unittest discover -s tests -v
```

预期结果：8 个技能格式有效，清单与中英文目录一致，内部资源可用，复制运行与缺失资源回归测试通过。这些检查不连接面板，也不安装任何组件。

手动加载时，将所需 skills/<name> 整个目录复制到 Agent 实际支持的技能目录，保留 references、许可证与 agents 配置，不能只复制 SKILL.md。Codex 用户技能根目录为 `~/.agents/skills`，Claude Code 项目级技能根目录为 `.claude/skills`。这是手动目录说明，不代表已安装或验证全部客户端。已有同名技能须先检查，避免覆盖。远程源码入口见本页仓库链接；版本 Release 和实际客户端验收另行记录。

配置好可信的既有 MCP 连接后，可以请求：

```text
使用 1panel-system，对我选定的面板执行只读检查。
分别报告观察事实、未知检查项和工具失败。
```

## 技能目录

| 技能 | 职责 | 触发示例 |
|---|---|---|
| [1panel-use](skills/1panel-use/SKILL.md) | 目标、能力发现和专业分流 | “检查这个 1Panel 服务器。” |
| [1panel-setup](skills/1panel-setup/SKILL.md) | 可信连接设置与有限诊断 | “API 连接失败了。” |
| [1panel-system](skills/1panel-system/SKILL.md) | 只读系统与仪表盘检查 | “检查资源情况。” |
| [1panel-websites](skills/1panel-websites/SKILL.md) | 网站列表及已授权静态/代理站点创建 | “创建这个指定的代理网站。” |
| [1panel-certificates](skills/1panel-certificates/SKILL.md) | 证书列表和有限签发 | “检查这个域名的证书期限。” |
| [1panel-databases](skills/1panel-databases/SKILL.md) | 支持范围内的检查与创建 | “在既有实例中创建这个数据库。” |
| [1panel-apps](skills/1panel-apps/SKILL.md) | 应用检查及已授权 MySQL/OpenResty 安装 | “检查已安装应用。” |
| [1panel-security-audit](skills/1panel-security-audit/SKILL.md) | 基于有限证据的只读风险审查 | “只审查风险，不改变服务器。” |

## 配置与兼容性

`.claude-plugin/plugin.json` 是技能源清单；`upstream.lock.json` 记录已检查的官方能力来源，不是二进制校验值，也不证明已安装。每个技能的可选 agents/openai.yaml 配置英文显示名称与显式调用提示，禁止存放 API 密钥。

支持相应 Agent Skills 加载方式的 Agent 可读取通用技能。本包包含 Codex 元数据和 Claude 包清单，具体客户端加载仍须独立验证。Cursor、OpenCode、Gemini 使用取决于实际技能发现配置，不能只凭目录存在宣称全部兼容。详见[使用与配置](docs/usage.zh-CN.md)。

## 维护与验证

```text
1panel-skills/
  .claude-plugin/plugin.json   技能源清单
  .github/workflows/          Windows/Linux 检查
  skills/<name>/             独立技能、引用、元数据与许可证
  scripts/                   格式和分发校验
  tests/                     复制运行与缺失资源回归
  docs/                      中英文使用与架构说明
  upstream.lock.json         已检查的官方来源身份
```

先更新本仓技能源码，再明确刷新插件快照并校验文件哈希。发布前执行 `python scripts/check_distribution.py --tracked`，要求资源在本仓 Git 中跟踪；不能把未提交快照标为不可变发布版。维护本包不会自动初始化 OpenSpec、Spec Kit 或 Harness。

结构校验不证明模型遵循技能、生产面板连接或客户端安装。插件仓库负责真实官方 MCP 与回环模拟 API 的集成验证。见[更新记录](CHANGELOG.md)、[维护规则](AGENTS.md)、[项目说明](CLAUDE.md)、[安全说明](SECURITY.md)、[贡献指南](CONTRIBUTING.md)、[来源声明](THIRD-PARTY-NOTICES.md)及[许可证](LICENSE)。

原创技能指引使用 Apache-2.0。上游 1Panel 和 mcp-1panel 保持 GPL-3.0；本包不复制其实现或二进制，不代表官方背书。
