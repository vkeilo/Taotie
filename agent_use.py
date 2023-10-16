import threading
import openai
import json
from config_parser import llm_name,support_llm_dict,key
from syslogger import logger
import zhipuai
import openai

class GptAgent():
    
    def __init__(self,model_name=llm_name):
        if model_name not in support_llm_dict:
            logger.error(f"model {model_name} not support")
        self.model = model_name
        self.interface_specification = support_llm_dict[self.model]['interface_specification']
        self.messages = []
        self.origin_memery = []
        self.init_api()
    
    # 根据模型初始化接口
    def init_api(self):
        if self.interface_specification == 'openai':
            # import openai
            openai.api_key = key
            if support_llm_dict[self.model]['url'] != "":
                openai.api_base = support_llm_dict[self.model]['url']
        elif self.interface_specification == 'zhipu':
            # import zhipuai
            zhipuai.api_key = key
        else:
            logger.error(f"model {self.model} not support")
        logger.info(f"api_base:{self.interface_specification}\tllm version: {self.model}")

    
    # 角色回滚
    def init_role(self):
        self.messages = self.origin_memery.copy()
        # print(self.messages)

    # 根据目标json对话中的内容进行角色扮演
    def init_messages_by_json(self,json_path):
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        self.messages = data["dialogues"]
        self.origin_memery = self.messages.copy()
        
    # 等待用户输入并与 GPT 进行交互
    def interact_with_agent(self):
        while True:
            user_input = input("You: \n")  # 等待用户输入
            if user_input.lower() == "exit":
                break  # 如果用户输入 "exit"，则退出交互
            self.prompt_add(user_input)  # 将用户输入添加到对话历史
            response = self.prompt_post()  # 获取 GPT 的回复
            print("assistant:", response)  # 打印 GPT 的回复

    def start_interact(self):
        check_thread = threading.Thread(target=self.interact_with_agent)
        check_thread.start()
            
    # 在对话历史中额外增加一句
    def history_add_one(self,role,text):
        self.messages.append({"role":role, "content": text})
         

    # 根据一段文本描述进行角色扮演
    def init_messages_by_roleplay(self,task):
        self.messages=None
        self.history_add_one("user",task)
        self.origin_memery = self.messages.copy()

    # 用户发问/出题    
    def prompt_add(self,text):
        self.history_add_one("user",text)

    # openai接口    
    def prompt_post_openai(self,T,maxtokens,remember_flag):
        # 调用API进行对话生成
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            max_tokens=maxtokens,
            temperature=T
        )
        # 提取生成的回复文本
        reply = response.choices[0].message.content
        self.history_add_one("assistant", reply)
        if not remember_flag:
            self.messages=self.messages[:-2]
        return reply
    # zhipuai 接口
    def prompt_post_zhipu(self,T ,maxtokens,remember_flag):
        # 调用API进行对话生成
        response = zhipuai.model_api.invoke(
            model=self.model,
            prompt=self.messages,
            temperature=T
        )
        # print((response))
        if response['success'] == False:
            logger.error(response)
        # 提取生成的回复文本
        reply = response['data']['choices'][0]['content']

        return reply[2:-1]
    
    # 接口整合
    def prompt_post(self,T = 0.1,maxtokens = 200,remember_flag = True ):
        logger.debug(f"post messages: {self.messages}")
        interface_specification = support_llm_dict[self.model]["interface_specification"]
        if self.interface_specification == 'zhipu':
            return self.prompt_post_zhipu(T,maxtokens,remember_flag)
        elif self.interface_specification == 'openai':
            return self.prompt_post_openai(T,maxtokens,remember_flag)
        else:
            logger.error(f"{interface_specification} 接口不支持")
        return ''
        
        