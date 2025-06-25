import os
import datetime
from dotenv import load_dotenv
import schedule
import time
from utils.git import GitHubClient
from utils.ai import summarize_repository_commits
from utils.report_generator import generate_report
from utils.plugins import load_and_run_plugins
from logger import logger

def load_config():
    """Load configuration from .env file"""
    load_dotenv()
    return {
        'github_token': os.getenv('GITHUB_TOKEN'),
        'github_username': os.getenv('GITHUB_USERNAME'),
        'github_orgs': os.getenv('GITHUB_ORG').split(','),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'openai_base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'report_time': os.getenv('REPORT_TIME', '09:00'),
        'generate_on_start': os.getenv('GENERATE_ON_START', 'false').lower() == 'true',
        'http_proxy': os.getenv('HTTP_PROXY', ''),
        'https_proxy': os.getenv('HTTPS_PROXY', ''),
        'timezone': os.getenv('TIMEZONE', 'Asia/Shanghai')
    }

def generate_daily_report():
    """Generate daily report for the previous day's commits"""
    try:
        logger.info("Starting daily report generation")
        config = load_config()
        
        # Calculate date range (previous day)
        today = datetime.datetime.now().date()
        yesterday = today - datetime.timedelta(days=1)
        date_str = yesterday.strftime('%Y-%m-%d')
        
        # Initialize GitHub client
        github_client = GitHubClient(config['github_username'], config['github_token'])
        github_client.set_proxy(config['http_proxy'], config['https_proxy'])
        
        # Get all repositories for the user
        repositories = github_client.get_user_repositories()
        
        for org in config['github_orgs']:
            repositories.extend(github_client.get_org_repositories(org))

        logger.info(f"Found {len(repositories)} repositories")
        
        repo_summaries = []
        
        # Process each repository
        for repo in repositories:
            logger.info(f"Processing repository: {repo['full_name']}")
            
            # Get commits for the previous day
            commits = github_client.get_commits_by_date_range(
                repo['full_name'],
                yesterday,
                today
            )
            
            if not commits:
                logger.info(f"No commits found for repository {repo['full_name']} in the given date range")
                continue
            
            # Summarize commits using AI
            repo_summary = summarize_repository_commits(
                repo['full_name'], 
                repo['description'],
                commits, 
                config['openai_api_key'],
                config['openai_base_url'],
                config['openai_model'],
                config['timezone']
            )
            
            repo_summaries.append(repo_summary)
            
        
        if not repo_summaries:
            logger.info("No commits found for the given date range")
            return
        
        # Generate the final report
        report = generate_report(repo_summaries, date_str, config['timezone'])
        
        report = load_and_run_plugins(report)

        logger.info("Finish")
        
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}", exc_info=True)

def main():
    """Main function to set up the scheduler"""
    config = load_config()
    report_time = config['report_time']
    
    logger.info(f"Scheduling daily report generation at {report_time}")
    schedule.every().day.at(report_time).do(generate_daily_report)
    
    # Generate report immediately if configured to do so
    if config['generate_on_start']:
        logger.info("Generating report on startup as configured")
        generate_daily_report()
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 