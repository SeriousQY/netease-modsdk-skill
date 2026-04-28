# mcmodapi Claude Code Skill

用于网易《我的世界》中国版 ModSDK / MCStudio AddOn 项目的 Claude Code 技能。它提供本地文档更新脚本和查询规则，帮助 Claude 优先检索 ModSDK API、事件、组件和示例。

## 重要说明

本仓库只发布查询工具与更新脚本，**不再分发** EaseCation/netease-modsdk-wiki 或官方文档的镜像内容。

文档内容不会提交到 GitHub。用户如需使用本地文档索引，请在自己的机器上运行更新脚本：

```bash
python scripts/update_docs.py
```

脚本会从公开来源下载文档到本地 `references/` 目录，并生成搜索索引。`references/` 已被 `.gitignore` 排除。

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

## 使用方式

将本目录放入 Claude Code skills 目录，例如：

```text
~/.claude/skills/mcmodapi
```

然后在 Claude Code 中询问 ModSDK API、事件、组件或示例即可触发该技能。
