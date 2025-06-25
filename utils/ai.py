import logging
import openai
from openai import OpenAI
import pytz
from datetime import datetime
from utils.prompt import get_commit_summary_prompt, SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def summarize_repository_commits(repo_name, repo_desc, commits, api_key, base_url, model, timezone='Asia/Shanghai'):
    """
    使用OpenAI总结仓库的提交记录
    
    Args:
        repo_name (str): 仓库名称
        repo_desc (str): 仓库描述
        commits (list): 提交信息字典列表
        api_key (str): OpenAI API密钥
        base_url (str): OpenAI API基础URL
        model (str): 要使用的OpenAI模型
        timezone (str): 时区字符串，默认为'Asia/Shanghai'
    
    Returns:
        dict: 仓库总结信息
    """
    if not commits:
        return {
            'repository': repo_name,
            'summary': "在指定时间段内未找到此仓库的提交记录。",
            'commit_count': 0,
            'commits': []
        }
    
    # 创建时区对象
    tz = pytz.timezone(timezone)
    
    # 创建用于提示的格式化提交信息
    commit_descriptions = []
    for commit in commits:
        # 转换日期时区
        commit_date = datetime.strptime(commit['date'], "%Y-%m-%dT%H:%M:%SZ")
        commit_date = pytz.utc.localize(commit_date).astimezone(tz)
        formatted_date = commit_date.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        files_text = ', '.join([f"{file['filename']} ({file['status']})" for file in commit['files']])
        commit_text = (
            f"Commit: {commit['sha'][:7]}\n"
            f"Author: {commit['author']} <{commit['email']}>\n"
            f"Date: {formatted_date}\n"
            f"Message: {commit['message']}\n"
            f"Files changed: {files_text}\n"
        )
        commit_descriptions.append(commit_text)
    
    all_commits_text = "\n\n".join(commit_descriptions)
    
    # 创建提示
    prompt = get_commit_summary_prompt(repo_name, repo_desc, all_commits_text)
    
    try:
        # 初始化OpenAI客户端
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # 调用OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        
        # 提取总结
        summary = response.choices[0].message.content.strip()
        
        repo_summary = {
            'repository': repo_name,
            'summary': summary,
            'commit_count': len(commits),
            'commits': commits
        }
        
        return repo_summary
        
    except Exception as e:
        logger.error(f"使用OpenAI总结提交时出错: {str(e)}")
        return {
            'repository': repo_name,
            'summary': f"生成总结失败: {str(e)}",
            'commit_count': len(commits),
            'commits': commits
        } 