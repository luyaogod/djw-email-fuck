from datetime import datetime, timedelta
import csv
import time
import logging
from config import (
    USERNAME,
    PASSWORD,
    EMAIL_CONTENT,
    WORK_CALENDAR,
    WORK_CALENDAR_ENCODING,
    TASK_TIME_HOUR,
    TASK_TIME_MINUTE,
    MAX_RESTART_COUNT,  # 新增最大重启次数配置项
)
from core import PostMan

# 配置日志记录
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WorkCalendar:
    """工作日历检查"""

    def __init__(self, csv_path: str, encoding: str = WORK_CALENDAR_ENCODING):
        self.work_days = set()
        self.non_work_days = set()
        with open(csv_path, encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                date_str = f"{row['年']}-{int(row['月']):02d}-{int(row['日']):02d}"
                if row["工作日"] == "是":
                    self.work_days.add(date_str)
                else:
                    self.non_work_days.add(date_str)

    def is_workday(self, check_date: datetime = None) -> bool:
        check_date = check_date or datetime.now()
        date_str = check_date.strftime("%Y-%m-%d")
        if date_str in self.work_days:
            return True
        if date_str in self.non_work_days:
            return False
        return check_date.weekday() < 5  # 默认周一到周五为工作日


def run_scheduler(task: callable, hour: int, minute: int):
    """主调度循环"""
    calendar = WorkCalendar(WORK_CALENDAR, WORK_CALENDAR_ENCODING)

    while True:
        now = datetime.now()
        # 计算今天的目标执行时间
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        # 如果今天已过目标时间，则计算明天的
        if now > target_time:
            target_time += timedelta(days=1)

        # 计算等待时间（秒）
        wait_seconds = (target_time - now).total_seconds()
        logger.info(f"下次执行时间: {target_time} (等待 {wait_seconds:.1f} 秒)")

        # 阻塞等待（支持Ctrl+C中断）
        try:
            time.sleep(wait_seconds)
        except KeyboardInterrupt:
            logger.info("定时任务已停止")
            raise  # 重新抛出以便外部处理

        # 执行任务（工作日检查）
        if calendar.is_workday():
            task()
            logger.info("任务执行完毕")
        else:
            logger.info("今天是休息日，任务跳过")


def main():
    """主程序入口，包含错误处理和重启机制"""
    restart_count = 0
    # 获取最大重启次数，如果未配置则默认为10
    max_restarts = MAX_RESTART_COUNT

    while restart_count < max_restarts:
        try:
            # 每次重启都重新初始化邮件发送器
            logger.info(f"启动邮件调度器 (尝试 #{restart_count + 1})")
            postman = PostMan(USERNAME, PASSWORD, EMAIL_CONTENT)
            logger.info("今天是工作日吗：%s", WorkCalendar(WORK_CALENDAR).is_workday())
            run_scheduler(postman.do_send_email, TASK_TIME_HOUR, TASK_TIME_MINUTE)
            break  # 如果正常退出则跳出循环
            
        except KeyboardInterrupt:
            logger.info("用户中断，程序终止")
            break
            
        except Exception as e:
            restart_count += 1
            logger.error(f"发生未捕获异常: {str(e)}")
            logger.exception("异常详情:")
            
            if restart_count < max_restarts:
                logger.warning(f"将在5秒后重启程序 ({restart_count}/{max_restarts})")
                try:
                    time.sleep(5)  # 避免频繁重启
                except KeyboardInterrupt:
                    logger.info("重启过程中被用户中断")
                    break
            else:
                logger.error(f"已达到最大重启次数 ({max_restarts})，程序终止")
                raise  # 抛出异常确保程序退出


if __name__ == "__main__":
    main()