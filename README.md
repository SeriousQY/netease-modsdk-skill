# mcmodapi Claude Code Skill

用于网易《我的世界》中国版 ModSDK / MCStudio AddOn 项目的 Claude Code 技能。它提供本地文档更新脚本和查询规则，帮助 Claude 优先检索 ModSDK API、事件、组件和示例。

## 重要说明

本仓库只发布查询工具与更新脚本，**不再分发** EaseCation/netease-modsdk-wiki 或官方文档的镜像内容。

文档内容不会提交到 GitHub。用户如需使用本地文档索引，需要在自己的机器上运行更新脚本。脚本会从公开来源下载文档到本地 `references/` 目录，并生成搜索索引。`references/` 已被 `.gitignore` 排除。

## 首次安装

### 方式一：直接克隆到 Claude Code skills 目录

macOS / Linux：

```bash
git clone https://github.com/<your-name>/netease-modsdk-skill.git ~/.claude/skills/mcmodapi
cd ~/.claude/skills/mcmodapi
python scripts/update_docs.py
```

Windows PowerShell：

```powershell
git clone https://github.com/<your-name>/netease-modsdk-skill.git "$env:USERPROFILE\.claude\skills\mcmodapi"
Set-Location "$env:USERPROFILE\.claude\skills\mcmodapi"
python scripts/update_docs.py
```

> 发布后请把上面的 `<your-name>` 替换为实际 GitHub 用户名或组织名。

### 方式二：手动下载

1. 从 GitHub 下载本仓库 ZIP。
2. 解压到 Claude Code skills 目录：
   - macOS / Linux: `~/.claude/skills/mcmodapi`
   - Windows: `%USERPROFILE%\.claude\skills\mcmodapi`
3. 在该目录运行：

```bash
python scripts/update_docs.py
```

## 下载或更新文档

首次安装后必须运行一次：

```bash
python scripts/update_docs.py
```

后续如果想刷新到上游最新文档，也运行同一条命令：

```bash
python scripts/update_docs.py
```

更新成功后，本地会生成：

```text
references/
  api-index.md
  interfaces.md
  events.md
  search-guide.md
  wiki/
```

这些文件只保存在本地，用于 Claude 查询，不建议提交或发布。

## 使用方式

安装并运行更新脚本后，在 Claude Code 中询问 ModSDK API、事件、组件或示例即可触发该技能。例如：

```text
/mcmodapi 查询 ListenForEvent 怎么用
/mcmodapi PlayerAttackEntityEvent 参数有哪些
/mcmodapi 服务端怎么创建实体
```

## 文档来源与权利归属

- 上游文档来源：EaseCation/netease-modsdk-wiki
- Context7 入口：上游 `docs/mcdocs/context7.json` 中声明的 Context7 页面
- 官方/上游文档的版权、商标和相关权利归其各自权利人所有

本项目不声称拥有上游文档内容，也不对上游文档进行再授权。更新脚本仅供用户在本地环境中按需下载公开内容用于查询。

## 查询策略

使用该技能时，Claude 应优先查询：

1. 本地生成索引：`references/api-index.md`、`references/interfaces.md`、`references/events.md`
2. 本地完整 Markdown 镜像：`references/wiki/docs/**/*.md`
3. Context7、GitHub、网页资料仅作为本地未命中或需要示例扩展时的补充来源

Context7 适合语义检索和示例摘要；本地镜像更适合精确核对 API 签名和引用来源。

## 文件结构

```text
mcmodapi/
  SKILL.md
  README.md
  .gitignore
  scripts/
    update_docs.py
```

运行更新脚本后会生成本地目录：

```text
references/
```

该目录包含镜像文档和生成索引，只应保存在本地，不建议发布。

## 故障排查

### `python` 命令不存在

尝试使用：

```bash
python3 scripts/update_docs.py
```

### 下载很慢或失败

脚本需要访问 GitHub。请确认网络可以访问：

```text
https://github.com/EaseCation/netease-modsdk-wiki
```

如果失败，稍后重试即可。