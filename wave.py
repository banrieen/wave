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

if __name__ == '__main__':
    main()
