---
name: mcmodapi
description: "用于网易《我的世界》中国版 ModSDK / MCStudio AddOn 项目的 API、事件、组件和示例查询。"
version: 0.1.0
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---

# mcmodapi

用于查询网易《我的世界》中国版 ModSDK 文档，并基于本地镜像文档提供代码指导。

## 适用范围

本技能覆盖从 `EaseCation/netease-modsdk-wiki` 镜像下来的全部 Markdown 文档，重点包括：

- `references/wiki/docs/` 下的完整上游文档
- `references/wiki/docs/mcdocs/1-ModAPI/` 下的 ModAPI 接口与事件文档
- `references/wiki/docs/api-tools/` 下的 API 工具页面
- 生成索引：`references/api-index.md`、`references/interfaces.md`、`references/events.md`

## 判断是否为 ModSDK 项目

当工作区出现以下任一特征时，应将其视为网易 ModSDK 项目：

- 存在 `studio.json`
- 存在匹配 `*_beh`、`*_res`、`*Scripts`、`netease_*` 的目录
- Python 代码导入 `from mod.common.mod import Mod`
- Python 代码导入 `import mod.client.extraClientApi as clientApi`
- Python 代码导入 `import mod.server.extraServerApi as serverApi`
- 代码中调用 `RegisterSystem`、`ListenForEvent`、`GetEngineCompFactory`、`CreateEngineCompFactory`、`BroadcastToServer`、`NotifyToClient`

只有在项目上下文不明确时，才使用 `Glob` 或 `Grep` 进一步确认这些特征。


## 与 Context7 的关系

`references/wiki/docs/mcdocs/context7.json` 只是指向 Context7 页面和 public key 的入口文件，不是完整文档本体。Context7 页面可提供大量语义片段和示例摘要，适合快速理解和补充搜索；但本技能的本地镜像包含完整上游 Markdown 文档、原始 `api-index.json` 以及生成索引，更适合精确查询、离线检索和引用来源。

查询优先级应为：

1. 本地生成索引：`api-index.md`、`interfaces.md`、`events.md`
2. 本地完整 Markdown 镜像：`references/wiki/docs/**/*.md`
3. Context7 页面或 GitHub/网页资料，仅在本地文档没有命中、需要语义补充或示例扩展时使用

回答时不要把 Context7 片段当作唯一权威来源；如果引用 Context7，应说明它是补充来源，并优先用本地 Markdown 或上游 GitHub 文档核对关键 API 签名。
## 查询流程

用户询问 ModSDK API、事件、组件或示例时，按以下顺序查询：

1. 优先搜索本地生成索引：
   - `references/api-index.md`：全部 API 与事件条目
   - `references/interfaces.md`：接口/API 条目
   - `references/events.md`：事件条目
2. 再搜索镜像的 Markdown 文档：
   - `references/wiki/docs/**/*.md`
   - 查询 API/事件细节时，优先看 `references/wiki/docs/mcdocs/1-ModAPI/**/*.md` 和 `references/wiki/docs/api-tools/*.md`
3. 先精确搜索标识符，再做模糊搜索。
4. 回答时优先引用本地文档，并给出本地 reference 文件链接。
5. 如果本地 `mcmodapi` 文档没有找到匹配项，先明确说明本地文档未包含该内容，再回退到 GitHub、网页或其他来源。

## 常用搜索模式

可在本技能目录内用 `Grep` 搜索以下模式：

- API 名称：`RegisterSystem|GetEngineCompFactory|CreateEngineCompFactory`
- 事件名称：`PlayerAttackEntityEvent|UiInitFinished|AchievementButtonMovedClientEvent`
- 端类型：`client|server`
- 常见 SDK 调用：`ListenForEvent|UnListenForEvent|BroadcastToServer|BroadcastToAllClient`

宽泛查询时，先检查生成索引，再搜索 `references/wiki`。

## 更新文档

运行以下命令刷新本地文档：

```bash
python C:/Users/Admin/.claude/skills/mcmodapi/scripts/update_docs.py
```

更新脚本会下载公开 GitHub 内容，将原始文档保存到 `references/wiki`，并重新生成可搜索的 Markdown 索引。脚本只使用 Python 标准库。

## 回答规范

回答 API 问题时：

- 说明是否在本地文档中找到该 API/事件。
- 如果文档中有端类型，标明 `client` / `server`。
- 给出方法名/事件名、参数摘要、返回值摘要和来源链接。
- 如果上游文本存在乱码或内容不完整，要明确说明不确定性。
- 不要自行猜测或修正乱码字段的中文含义。


