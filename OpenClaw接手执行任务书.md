# OpenClaw 接手执行任务书

## 1. 你的任务定位

你不是从零设计这个项目。

你现在要做的是：基于已经搭好的 `ai-news-assistant` 仓库骨架，继续完成飞书接入和可运行联调。

你应将当前任务理解为：

- 已完成：产品方案、Skill 骨架、Prompt 资产、模板、示例、最小 CLI 入口、飞书接入基础结构
- 你要完成：飞书真实联通、表格/文档创建与写入、OpenClaw 实际调用链路打通

## 2. 仓库位置

- 项目根目录：`D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant`

## 3. 你必须先阅读的文件

### 核心说明

- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\README.md`
- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\SKILL.md`

### 设计与配置

- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\config\default-config.json`
- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\config\feishu-schema.md`

### 飞书接入基础代码

- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\ai_news_assistant\feishu.py`
- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\scripts\feishu_sync.py`
- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\tests\test_feishu.py`

### 其他流程入口

- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\scripts\ingest_news.py`
- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\scripts\generate_note.py`
- `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\scripts\generate_script.py`

## 4. 当前已完成状态

当前仓库已经具备：

- OpenClaw 可安装 skill/repo 的基础目录结构
- `SKILL.md` 中的产品身份和主流程定义
- Feishu Bitable / Feishu Docs 的字段和文档模板设计
- 飞书环境变量加载与校验逻辑
- 飞书鉴权请求、多维表格写入请求、文档创建请求的请求组装逻辑
- 基础测试已通过

## 5. 你下一步必须完成的事情

### 任务一：接通飞书真实 API

你需要在现有 `feishu.py` 基础上补全：

- 获取 tenant access token
- 发送真实 HTTP 请求
- 创建飞书文档
- 向飞书多维表格插入记录
- 返回真实响应结果

要求：

- 不要推翻现有结构
- 在现有请求构造函数基础上继续实现
- 保持配置通过环境变量读取

### 任务二：完成飞书初始化流程

你需要让系统可以完成最小初始化检查：

- 验证飞书权限是否可用
- 验证目标多维表格是否存在
- 验证目标文档目录是否存在
- 如果项目允许自动创建，则创建所需文档和基础结构

### 任务三：让 CLI 具备真实执行能力

你需要增强 `scripts\feishu_sync.py`：

- `--mode check`：执行真实连通性检查
- `--mode bitable`：真实写入一条测试记录
- `--mode doc`：真实创建一篇测试文档

### 任务四：把资讯主流程逐步接到飞书

你需要从最小主链路开始打通：

1. `ingest_news.py`
   - 解析输入
   - 产出标准化资讯对象
   - 写入飞书资讯主表
   - 写入飞书日报文档

2. `generate_note.py`
   - 从资讯和会话数据生成结构化笔记
   - 写入飞书笔记文档
   - 回填笔记链接

3. `generate_script.py`
   - 从笔记生成口播稿
   - 写入飞书文档
   - 回填口播稿链接

## 6. 你的边界

你不要做这些事：

- 不要重新设计产品方案
- 不要更换整体架构
- 不要把飞书换成别的主存储
- 不要删除已存在的 prompts/templates/examples
- 不要擅自把“单条资讯”为最小单位改掉

## 7. 你需要遵守的原则

- 用户只和 OpenClaw 聊天，不手动触发 skill 细节
- 单条资讯是最小工作单元
- 飞书多维表格负责流程状态
- 飞书文档负责内容承载
- 旧 ai-news 系列能力是后台模块，不是用户入口

## 8. 你的最小成功标准

你完成后，至少应该能现场跑通下面这条链路：

1. 用户输入一条或多条资讯
2. 系统拆条并写入飞书资讯主表
3. 系统把内容写入飞书日报文档
4. 用户指定某条资讯
5. 系统围绕该条资讯生成一篇独立笔记文档
6. 系统基于该笔记生成一篇口播稿文档

## 9. 你开始工作前的第一句自检

你必须先确认：

- 我是否已经阅读仓库根 README 和 SKILL
- 我是否已经阅读飞书配置和接入代码
- 我是否是在现有骨架上继续实现，而不是从零重来

如果答案不是“是”，不要开始修改。
