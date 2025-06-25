"""
提交总结的提示模板
"""

SYSTEM_PROMPT = """
你是一个有用的助手，可以总结git提交。请提供简洁、信息丰富的总结。
"""

def get_commit_summary_prompt(repo_name, repo_desc, all_commits_text):
    """
    获取用于总结仓库提交的提示模板
    
    Args:
        repo_name (str): 仓库名称
        all_commits_text (str): 所有提交的文本描述
    
    Returns:
        str: 格式化的提示模板
    """
    prompt = f"""
### 仓库名称：{repo_name}
### 仓库描述：{repo_desc}
    
### 要求：
- 每条工作内容以列表形式展示，格式为“日期 时间: 提交信息（简要总结）”。
- “提交信息（简要总结）”要简化并提炼关键信息，避免原样复制。
- 如果有多条commit，按时间顺序（从早到晚）排列。
- 严格按照模板格式输出（方括号的内容替换）。
- 只输出最终报告内容，不要解释和补充说明。

### 返回模板：
    
** [项目名（根据仓库描述生成）1] **

- ✅06-23 12:00: [提交信息1(简要总结)]
- ✅MM-DD xx:xx: [提交信息2(简要总结)]

** [项目名（根据仓库描述生成）2] **
..

### 提交记录：
{all_commits_text}
"""
    return prompt 