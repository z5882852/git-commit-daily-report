import requests
import logging

logger = logging.getLogger(__name__)

class GitHubClient:
    """GitHub API客户端，用于获取仓库和提交记录"""
    
    def __init__(self, username, token=None):
        """
        初始化GitHubClient
        
        Args:
            username (str): GitHub用户名
            token (str, optional): GitHub个人访问令牌
        """
        self.username = username
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({'Authorization': f'token {token}'})
    
    def set_proxy(self, http_proxy, https_proxy):
        """
        为会话设置代理
        
        Args:
            http_proxy (str): HTTP代理URL
            https_proxy (str): HTTPS代理URL
        """
        self.session.proxies.update({
            'http': http_proxy,
            'https': https_proxy
        })
    
    def clear_proxy(self):
        """
        清除会话代理
        """
        self.session.proxies.clear()
    
    def get_user_repositories(self):
        """
        获取用户的所有仓库
        
        Returns:
            list: 仓库信息字典列表
        """
        url = f"https://api.github.com/users/{self.username}/repos"
        
        repositories = []
        page = 1
        
        while True:
            params = {'page': page, 'per_page': 100}
            response = self.session.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"获取仓库失败: {response.status_code} - {response.text}")
                break
            
            repos_page = response.json()
            if not repos_page:
                break
                
            repositories.extend(repos_page)
            page += 1
        
        # 如果需要，过滤掉fork的仓库
        # repositories = [repo for repo in repositories if not repo['fork']]
        
        return repositories
    
    def get_org_repositories(self, org_name):
        """
        获取组织的所有仓库
        
        Returns:
            list: 仓库信息字典列表
        """
        url = f"https://api.github.com/orgs/{org_name}/repos"
        repositories = []
        page = 1
        while True:
            params = {'page': page, 'per_page': 100}
            response = self.session.get(url, params=params)
            if response.status_code != 200:
                logger.error(f"获取仓库失败: {response.status_code} - {response.text}")
                break
            repos_page = response.json()
            if not repos_page:
                break
            repositories.extend(repos_page)
            page += 1
        return repositories

    def get_commits_by_date_range(self, repo_name, start_date, end_date):
        """
        获取仓库在日期范围内用户的提交
        
        Args:
            repo_name (str): 仓库名称
            start_date (datetime.date): 开始日期（包含）
            end_date (datetime.date): 结束日期（不包含）
        
        Returns:
            list: 提交信息字典列表
        """
        # 格式化日期以适应GitHub API
        start_date_str = start_date.strftime('%Y-%m-%dT00:00:00Z')
        end_date_str = end_date.strftime('%Y-%m-%dT00:00:00Z')
        
        url = f"https://api.github.com/repos/{repo_name}/commits"
        
        params = {
            'author': self.username,
            'since': start_date_str,
            'until': end_date_str,
            'per_page': 100
        }
        
        commits = []
        page = 1
        
        while True:
            params['page'] = page
            response = self.session.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"获取{repo_name}的提交失败: {response.status_code} - {response.text}")
                break
            
            commits_page = response.json()
            if not commits_page:
                break
                
            for commit in commits_page:
                try:
                    # 获取每个提交的详细信息以获取文件更改
                    detailed_commit = self.get_detailed_commit(repo_name, commit['sha'])
                    commits.append(detailed_commit)
                except Exception as e:
                    logger.error(f"获取提交{commit['sha']}的详细信息时出错: {str(e)}")
            
            page += 1
        
        return commits
    
    def get_detailed_commit(self, repo_name, commit_sha):
        """
        获取特定提交的详细信息，包括文件更改
        
        Args:
            repo_name (str): 仓库名称
            commit_sha (str): 提交SHA
        
        Returns:
            dict: 包含文件更改的提交信息
        """
        url = f"https://api.github.com/repos/{repo_name}/commits/{commit_sha}"
        
        response = self.session.get(url)
        
        if response.status_code != 200:
            logger.error(f"获取详细提交失败: {response.status_code} - {response.text}")
            raise Exception(f"获取详细提交失败: {response.status_code}")
        
        detailed_commit = response.json()
        
        # 提取相关字段
        commit_info = {
            'sha': detailed_commit['sha'],
            'author': detailed_commit['commit']['author']['name'],
            'email': detailed_commit['commit']['author']['email'],
            'date': detailed_commit['commit']['author']['date'],
            'message': detailed_commit['commit']['message'],
            'files': [
                {
                    'filename': file['filename'],
                    'status': file['status'],
                    'additions': file['additions'],
                    'deletions': file['deletions'],
                }
                for file in detailed_commit.get('files', [])
            ],
            'repository': repo_name
        }
        
        return commit_info

# 辅助函数，用于保持向后兼容性
def get_user_repositories(username, token):
    """向后兼容函数"""
    client = GitHubClient(username, token)
    return client.get_user_repositories()

def get_commits_by_date_range(repo_name, username, token, start_date, end_date):
    """向后兼容函数"""
    client = GitHubClient(username, token)
    return client.get_commits_by_date_range(repo_name, start_date, end_date)

def get_detailed_commit(username, repo_name, commit_sha, token):
    """向后兼容函数"""
    client = GitHubClient(username, token)
    return client.get_detailed_commit(repo_name, commit_sha) 