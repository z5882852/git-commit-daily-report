import os
import datetime
from logger import logger




def run(report):
    date_str = datetime.datetime.now().date().strftime('%Y-%m-%d')
    output_folder = os.getenv('OUTPUT_FOLDER', 'reports')

    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the report
    report_filename = os.path.join(output_folder, f"commit_report_{date_str}.md")
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    logger.info(f"Report generated successfully: {report_filename}")