# ai-news 来源索引

本目录用于给 `2026-04-02_AI资讯助手` 建立一个可直达的旧版能力索引。

## 来源根目录

- 原始路径：`C:\Users\TyongLiu\skills.sh管理\archives\AIProject\_archived_duplicate_management_20260326\.claude\skills\_archived_superseded_20260326\ai-news`
- 根目录快捷入口：`ai-news_来源根目录.url`

## 结构总览

### 1. `ainews`

- 用途：自动抓取腾讯研究院微信公众号最新的《腾讯研究院AI速递》并落盘。
- 快捷入口：`01_ainews_目录.url`
- 关键文件：`01_ainews_SKILL.url`

### 2. `ainews-companion`

- 用途：围绕单条资讯做阅读陪伴、追问、背景补充与认知草稿沉淀。
- 快捷入口：`02_ainews-companion_目录.url`
- 关键文件：`02_ainews-companion_SKILL.url`

### 3. `ainews-archive`

- 用途：将阅读后的认知草稿归档进 PARA 结构，并更新导航与清理资源。
- 快捷入口：`03_ainews-archive_目录.url`
- 关键文件：`03_ainews-archive_SKILL.url`

### 4. `XHIP-agent`

- 用途：把文章或笔记转成“晓辉博士”风格短视频口播稿。
- 快捷入口：`04_XHIP-agent_目录.url`
- 关键文件：`04_XHIP-agent_SKILL.url`

## XHIP-agent 附加内容

- 输出样例位于源目录下 `outputs`
- 资源文件位于源目录下 `resources`
- 生成脚本位于源目录下 `scripts\generate_xiaohui_script.py`

## 说明

由于当前环境不能直接创建管理员权限要求的目录符号链接，这里采用 `.url` 快捷入口方式。
你在这个文件夹里双击对应入口，就可以直接打开原始目录或原始文件内容。
