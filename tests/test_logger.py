import shutil
import time
from pathlib import Path
import pytest
from app.core.logger import init_logger, get_logger, logger


@pytest.fixture(scope="module", autouse=True)
def setup_logger():
    init_logger()
    logger.info("Test logger....")
    yield
    # 测试结束后可清理日志文件（如果需要）
    log_dir = Path("./logs")
    if log_dir.exists() and log_dir.is_dir():
        shutil.rmtree(log_dir)


def test_logger_writes_log():
    log_path = Path("./logs/run.log")
    run_logger = get_logger(
        name="run",
        file_name=str(log_path),
        format_type="text",
        rotation="time",
    )
    test_msg = "test run logger..."
    run_logger.info(test_msg)
    time.sleep(1)  # 确保日志异步写入完成

    assert log_path.exists()
    content = log_path.read_text(encoding="utf-8")
    assert test_msg in content


def test_custom_logger_writes_json_log():
    log_path = Path("./logs/db.log")
    db_logger = get_logger(
        name="database",
        file_name=str(log_path),
        format_type="json",

        rotation="size",
        max_bytes=1024 * 1024,
        backup_count=3,
    )
    test_msg = "test run db logger..."
    db_logger.error(test_msg)
    time.sleep(1)  # 确保日志异步写入完成

    assert log_path.exists()
    content = log_path.read_text(encoding="utf-8")
    assert test_msg in content
    assert '"message":' in content  # 简单确认是 json 格式
