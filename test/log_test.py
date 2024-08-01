from loguru import logger
import sys

# 移除默认的 stderr 处理器
logger.remove(handler_id=None)

# 配置日志输出到控制台，仅输出 INFO 级别的日志
logger.add(
    sys.stdout,
    level="INFO",
    backtrace=False,  # 关闭堆栈跟踪信息，以避免重复输出
    diagnose=True   # 关闭诊断信息，以避免重复输出
)


# 示例代码
def example_function():
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")

if __name__ == "__main__":
    example_function()
