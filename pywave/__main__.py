#!.venv/bin/python
"""系统终端命令
支持Bash
数据源管理
数据加载
数据生成

"""

from pathlib import Path
import click

@click.command()
@click.option('--count', default=1, help='Number of rows.')
@click.option('--type', prompt='Data type',
              help='The count to rand that type data.')
def main(count, type):
    """Simple program that generate the count for datas of type."""
    for x in range(count):
        click.echo(f"Generrating {type}!")
# Merge old
# from src.csv2mysql import (
#       get_conf,
#       insert_info_table,
#       insert_list_table,
#       sync_to_sql,
#       runner,
#       )

# def cli_cmds():
#     parser = argparse.ArgumentParser(description='Please input project hostname and configuration file.')
#     parser.add_argument('-p', '--pro', metavar='project', type=str, default='default',
#                         help='hostname like zhaochi or qianzhao',required=True)
#     parser.add_argument('-c', '--conf', metavar='confpath', type=str, default=r'default.toml',
#                         help='conf file path',required=True)
#     parser.add_argument('-m', '--merge', metavar='confpath', type=str, default=r'true',
#                         help='merge the info schema into dut list ',required=False)
#     cmds = vars(parser.parse_args())
#     return cmds   

# def main(args=None):
#     try:
#        cmds = cli_cmds()
#     except argparse.ArgumentError:
#         print('Catching an argumentError') 
#     else:
#        print('Catching an parserError')
#     project = cmds["pro"] if len(cmds["pro"]) else "default"   
#     conf_file = os.path.abspath(cmds["conf"]) if os.path.exists(os.path.abspath(cmds["conf"])) else os.path.abspath(r"conf/default.toml")
#     runner(conf_file, project)

if __name__ == '__main__':
    print("""            """)
    main()

# # from pathlib import Path
# # from generater import rand_task

# import click

# @click.command()
# @click.option('--count', default=1, help='Number of rows.')
# @click.option('--type', prompt='Data type',
#               help='The count to rand that type data.')
# def main(count, type):
#     """Simple program that generate the count for datas of type."""
#     for x in range(count):
#         click.echo(f"Generrating {type}!")

