# 该模块解析 config.json 中的内容，并构建对应的全局变量
import json
import os

def get_config(file_name):
    with open(file_name, 'r') as f:
        config = json.load(f)
    return config



dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, 'config.json')
config = get_config(config_path)
support_llm_dict = config['support_llm']
llm_name = config['llm_name']
local_roles = config['local_roles']
keys = {model_name:model_message["key"] if  "key" in model_message else  ""  for model_name, model_message in support_llm_dict.items()}