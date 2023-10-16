# 该模块解析 config.json 中的内容，并构建对应的全局变量
import json


def get_config(file_name):
    with open(file_name, 'r') as f:
        config = json.load(f)
    return config

config = get_config('config.json')
support_llm_dict = config['support_llm']
llm_name = config['llm_name']
local_roles = config['local_roles']
key = config['key']