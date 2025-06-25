import logging
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

def generate_report(repo_summaries, date_str, timezone='Asia/Shanghai'):
    """
    根据仓库摘要生成Markdown格式报告
    
    Args:
        repo_summaries (list): 仓库摘要字典列表
        date_str (str): 报告的日期字符串 (YYYY-MM-DD)
        timezone (str): 时区字符串，默认为'Asia/Shanghai'
    
    Returns:
        str: Markdown格式的报告
    """
    try:
        # 格式化标题的日期
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        tz = pytz.timezone(timezone)
        date_obj = tz.localize(date_obj)
        formatted_date = date_obj.strftime("%Y年%m月%d日 %H:%M:%S %Z")
        
        # 计算提交总数
        total_commits = sum(repo['commit_count'] for repo in repo_summaries)
        
        # 生成报告头部
        report = f"""# 代码提交日报 {formatted_date}

## 概览
- **日期**: {formatted_date}
- **仓库数量**: {len(repo_summaries)}
- **提交总数**: {total_commits}

## 具体工作
"""
        
        # 为每个仓库添加摘要
        for repo in repo_summaries:
            report += f"""{repo['summary']}
"""         
            if False:
                report += f"\n### 详细提交\n"
                # 添加单个提交
                for commit in repo['commits']:
                    commit_date = datetime.strptime(commit['date'], "%Y-%m-%dT%H:%M:%SZ")
                    commit_date = pytz.utc.localize(commit_date).astimezone(tz)
                    commit_date = commit_date.strftime("%Y-%m-%d %H:%M:%S %Z")
                    files_changed = len(commit['files'])
                    additions = sum(file.get('additions', 0) for file in commit['files'])
                    deletions = sum(file.get('deletions', 0) for file in commit['files'])
                    
                    report += f"""
    - **{commit['sha'][:7]}** - {commit_date}
    - **消息**: {commit['message'].splitlines()[0]}
    - **文件**: {files_changed} 个文件修改 (+{additions}, -{deletions})
    """
        
        return report
    
    except Exception as e:
        logger.error(f"生成报告时出错: {str(e)}")
        return f"# 生成报告出错\n\n生成日报时发生错误: {str(e)}" 