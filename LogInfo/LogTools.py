#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import sys


class Logger(object):
    # 设置全局默认的日志文件位置
    DEFAULT_LOG_DIRECTORY = 'LogInfo'
    '''
    Log日志类
    '''

    def __init__(self, filename=None):

        self.filename = self.creat_log(filename)
        self.console = sys.stdout

    def creat_log(self, filename):
        '''
        指定log 日志路径
        :param filename:
        :return:
        '''
        if filename:
            filename = filename
        else:
            filename = 'app.log'
            script_directory = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(script_directory, filename)
        return filename

    def log(self, message, level='INFO', encoding='utf-8'):

        '''
        日志说明
        :param message: 信息
        :param level:  默认INFO
        :param encoding: 默认编码
        :return:
        '''
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        level_color = '\033[91m' if level == 'ERROR' else '\033[92m' if level == 'WARNING' else '\033[93m'
        level_color += level + '\033[0m'
        message_formatted = f'[{timestamp}] {level_color}: {message}\n'
        self.console.write(message_formatted)

        level_color_log = level if level in ('ERROR', 'WARNING') else 'INFO'
        message_formatted_log = f'[{timestamp}] {level_color_log}: {message}\n'
        try:
            if self.filename:
                with open(self.filename, 'a', encoding=encoding, errors='ignore') as file:
                    file.write(message_formatted_log)
                    file.flush()  # 确保立即将数据写入磁盘
            else:
                os.makedirs(os.path.dirname(self.filename), exist_ok=True)
                with open(self.filename, 'a', encoding=encoding, errors='ignore') as file:
                    file.write(message_formatted_log)
                    file.flush()  # 确保立即将数据写入磁盘
        except IOError as e:
            print(f"I/O错误: {e}")  # 可以根据实际情况进行更复杂的错误处理

    def info(self, message):
        self.log(message, 'INFO')

    def error(self, message):
        self.log(message, 'ERROR')

    def warning(self, message):
        self.log(message, 'WARNING')

# if __name__ == '__main__':
#     logger = Logger('app.log')
#     logger.info(F'汉字123213')
#     logger.error('This is an error message.')
#     logger.warning('This is a warning message.')
