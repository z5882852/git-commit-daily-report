import os
from logger import logger
from dotenv import load_dotenv
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *

load_dotenv()


def commit_record(report):
    client = lark.Client.builder() \
        .app_id(os.getenv("FEISHU_APP_ID")) \
        .app_secret(os.getenv("FEISHU_APP_SECRET")) \
        .build()

    request: CreateAppTableRecordRequest = (
        CreateAppTableRecordRequest.builder()
        .app_token(os.getenv("APP_TOKEN"))
        .table_id(os.getenv("TABLE_ID"))
        .request_body(
            AppTableRecord.builder()
            .fields({"日报内容": report})
            .build()
        )
        .build()
    )
    response: CreateAppTableRecordResponse = client.bitable.v1.app_table_record.create(request)

    # 处理失败返回
    if not response.success():
        raise Exception(f"client.bitable.v1.app_table_record.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")



def run(report):
    """
    发送报告到飞书
    """
    commit_record(report)

if __name__ == "__main__":
    run("test")