# -*- coding: utf-8 -*-
# src Python Library for personaly ETL, (C)
# 2023,2025 Thomas.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=too-many-lines,disable=too-many-branches,too-many-statements
# pylint: disable=too-many-arguments

from src.mysqlSync import mysql_sync
# from src.csvParser import (get_csv_filelist,
#             extract_csv,
#             parse_dut_info,
#             parse_dut_list,
#             )
from src.csvParser import csvParser
from src.csv2mysql import (
      get_conf,
      insert_dict_table,
      sync_to_sql,
      runner,
      )

print("""
 ____                        
/ ___| _ __  _ __ __ _ _   _ 
\___ \| '_ \| '__/ _` | | | |
 ___) | |_) | | | (_| | |_| |
|____/| .__/|_|  \__,_|\__, |
      |_|              |___/ 
      """)
