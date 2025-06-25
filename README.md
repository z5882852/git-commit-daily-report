# Git Commit Daily Report
> 该README由AI生成。
这是一个自动化工具，用于生成用户在GitHub上的每日代码提交报告。该工具会在指定时间（默认每天上午9点）自动查询指定GitHub用户前一天的所有代码提交，然后使用OpenAI API生成一份详细的日报。

## 功能特点

- 自动获取指定GitHub用户的所有仓库
- 筛选指定时间范围内的提交记录
- 使用OpenAI对每个仓库的提交进行智能总结
- 生成结构化的Markdown格式日报
- 支持定时自动运行

## 安装要求

- Python 3.8+

## 安装步骤

1. 克隆代码库

```bash
git clone <repository-url>
cd git-commit-report
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置环境变量

复制示例环境文件并编辑:

```bash
cp .env.example .env
```

编辑`.env`文件，填入以下信息:
- GitHub个人访问令牌 (GITHUB_TOKEN)
- GitHub用户名 (GITHUB_USERNAME)
- OpenAI API密钥 (OPENAI_API_KEY)
- 其他可选设置

## 使用方法

### 启动自动任务

运行以下命令启动自动任务，将在配置的时间（默认每天9:00）生成报告:

```bash
python main.py
```

### 手动生成报告

如果需要立即生成报告，可以编辑`main.py`文件，取消注释以下行:

```python
# 取消注释以下行来立即生成报告
# generate_daily_report()
```

然后运行:

```bash
python main.py
```

## 配置选项

在`.env`文件中可以配置以下选项:

- `GITHUB_TOKEN`: GitHub个人访问令牌
- `GITHUB_USERNAME`: GitHub用户名
- `GITHUB_ORG`: GitHub组织名称，多个组织可用逗号分隔
- `OPENAI_API_KEY`: OpenAI API密钥
- `OPENAI_BASE_URL`: OpenAI API基础URL (默认: https://api.openai.com/v1)
- `OPENAI_MODEL`: 使用的OpenAI模型 (默认: gpt-3.5-turbo)
- `REPORT_TIME`: 每日生成报告的时间 (默认: 09:00)
- `OUTPUT_FOLDER`: 报告输出目录 (默认: reports)
- `GENERATE_ON_START`: 启动程序时立即生成报告 (默认: false)
- `HTTP_PROXY`: HTTP代理设置（如有需要）
- `HTTPS_PROXY`: HTTPS代理设置（如有需要）
- `TIMEZONE`: 时区设置 (默认: Asia/Shanghai)

## 报告格式

生成的报告为Markdown格式，包含以下内容:

- 日期概览
- 总体提交统计
- 按仓库分类的代码提交总结
- 每个仓库的详细提交记录
  - 提交SHA
  - 提交时间
  - 提交消息
  - 更改统计

## 注意事项

- 确保GitHub令牌有足够的权限读取仓库信息
- 设置适当的OpenAI API使用限制
- 生成的报告将保存在`reports`目录中 (可配置)

## 插件系统

本工具支持插件系统，可以通过插件扩展报告生成后的处理功能。插件位于 `plugins/` 目录下，每个插件都是一个独立的 Python 模块。

### 插件开发

要创建一个新插件，只需在 `plugins/` 目录下创建一个新的 `.py` 文件，并实现 `run(report)` 函数。该函数接收报告内容作为字符串参数，并可以返回修改后的报告内容。

插件示例：

```python
# plugins/example_plugin.py
def run(report):
    """
    插件入口函数
    
    Args:
        report (str): 原始报告内容
    
    Returns:
        str: 修改后的报告内容
    """
    # 在报告末尾添加签名
    return report + "\n\n---\n*由示例插件生成*"
```

### 内置插件

系统自带以下示例插件：

1. `example_plugin.py`: 在报告末尾添加签名和时间戳
2. `email_sender.py`: 将生成的报告发送到指定的邮箱

邮件发送插件需要在 `.env` 文件中添加以下配置：

```
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
SENDER_EMAIL=sender@example.com
RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com 