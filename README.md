# AI资讯助手

## 项目定位

一个面向 AI 行业资讯采集、筛选、整理与解读的助手型项目。

## OpenClaw 接手入口

如果由 OpenClaw 接手继续搭建，请优先阅读以下文件：

1. `OpenClaw学习指令_AI资讯助手.md`
2. `OpenClaw接手执行任务书.md`
3. `ai-news-assistant/README.md`
4. `ai-news-assistant/SKILL.md`

当前真正需要继续开发的核心目录是：

- `ai-news-assistant/`

## 初始目标

- 聚合多渠道 AI 资讯
- 快速提炼重点信息
- 输出适合分享或存档的内容摘要

## 后续可扩展方向

- 资讯源管理
- 自动摘要与标签分类
- 每日/每周资讯简报
- 面向公众号或社群的内容改写

## 当前仓库状态

当前已经完成：

- 产品方案文档
- OpenClaw 学习指令
- OpenClaw 接手执行任务书
- `ai-news-assistant` 可安装仓库骨架
- 飞书接入最小代码骨架
- 基础测试

当前尚未完成：

- 飞书真实 API 写入联通
- 多维表格真实建表/写表
- 飞书文档真实创建与更新
- 将主流程完整接入 OpenClaw 执行链路

## 推荐下一步

下一步由 OpenClaw 接手时，应只做一件事：

- 在现有 `ai-news-assistant` 骨架基础上，继续补完飞书真实接入和主链路联调
