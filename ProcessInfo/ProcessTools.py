#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import shutil
import subprocess
import time
import traceback


class ProcessCure(object):
    '''
    windows 进程工具
    '''

    def admin_kill_process(self, process_name, timeout=1800000):
        '''
        使用admin结束进程
        :param process_name: 进程名称
        :return: 进程已经结束
        '''
        f = None
        exe_name = process_name.split('.')[0]
        os.makedirs(exe_name, exist_ok=True)
        exe_name_folder = exe_name

        try:
            bat = F'{os.getcwd()}{os.sep}{exe_name_folder}{os.sep}{exe_name}.bat'
            f = open(bat, 'w')
            f.write(f'taskkill /IM  {process_name} /f')
        except Exception as e:
            traceback.print_exc()
            raise e
        finally:
            if f:
                f.close()

        try:
            self.creat_vbs_info(exe_name)
            shell = F'{os.getcwd()}{os.sep}{exe_name_folder}{os.sep}{exe_name}.vbs'

            sp = subprocess.Popen(
                shell,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            sp.wait(timeout=timeout)

            stderr = str(sp.stderr.read().decode('gbk')).strip()
            stdout = str(sp.stdout.read().decode('gbk')).strip()
            if '' != stderr:
                raise Exception(stderr)
            if stdout.find('失败') > -1:
                raise Exception(stdout)
        except Exception as e:
            raise e
        time.sleep(1)
        shutil.rmtree(exe_name)
        return F'{process_name}进程已经结束'

    def creat_vbs_info(self, exe_name):
        '''
        创建vbs文件,并写入内容
        :param exe_name: exe名称
        :return: vbs_info 路径
        '''
        exe_name_folder = exe_name
        # 这里的bat路径是当前路径
        vbs_info = F'''
        cwd = CreateObject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
        path = cwd & "{os.sep}{exe_name}.bat"

        Set shell = CreateObject("Shell.Application")
        shell.ShellExecute path, "", "", "runas", 1

        WScript.Quit
        '''
        vbs_path = F'{os.getcwd()}{os.sep}{exe_name_folder}{os.sep}{exe_name}.vbs'
        if os.path.exists(vbs_path):
            os.remove(vbs_path)
        f = open(vbs_path, 'w')
        f.write(f'{vbs_info}')
        return vbs_info


# if __name__ == '__main__':
#     process_name = 'iscpclient.exe'
#     PT = ProcessCure()
#     PT.admin_kill_process(process_name)
