# Taotie
A tool that integrates a variety of LLM api.

## support LLM interfaces
support LLM interfaces can be found in `config.json`
|support LLM interfaces| interface type |
|:---:|:---:|
| chatglm2-6b | openai |
| chatglm_pro | zhipu |
| chatglm_std | zhipu |
| chatglm_lite | zhipu |

# Interface usage guide
## Dependency installation
---------
At first we need to install the dependencies.
```bash
pip install -r requirements.txt
```
</br>

## Init agent object
-------
You can init an agent object by using the following code.
```python
from agent_use import ChatAgent
my_agent = ChatAgent()
```
When class ChatAgent is initialized, it will take the value of `llm_name` in file `config.json` as the default LLM api.  
If you want to use other LLM-api, you can set the `llm_name` in file `config.json` to the name of the LLM api you want, or you can just set `llm_name` variable like this:
```python
from agent_use import ChatAgent
my_agent = ChatAgent(llm_name='chatglm2-6b')
```
Make sure that the the LLM api you want to use is surpported by `config.json`. 

</br>

## Chat with you agent
-------
After init the agent object, you can chat with your agent by using the following code.
```python
my_agent.prompt_add('Hello')
response = my_agent.prompt_post(T=0.1, maxtokens=200, remember_flag=False)
```
`prompt_post()` supports 3 parameters: 

| Parameter | defaut value | Description |
| --------- |-----------| ----------- |
|T| 0.1 |Model sampling temperature, most LLM api will use this parameter to control the model sampling probability.|
|maxtokens| 200 |Maximum number of tokens to generate.Not take effect to all LLM api.|
remember_flag| True |If True, the agent will recode this dialogue as history conversation|

If you want specify your agent for roleplay base a simple sentence, you can run the following code after initializing the agent object.
```python
my_agent.init_messages_by_sentence("You are a cat. From now on, the words you say will have a cat's tone words at the end")
```
At most time, you may need you agent to deal with more complex tasks, so you will want use a series of dialogue to specify your agent for roleplay, in this case, use `init_messages_by_json()` instead of `init_messages_by_sentence()`.
```python
my_agent.init_messages_by_json('your_dialogue_json_file.json')
```
The content of the dialogue json file should have the following format, and make sure user and assistant take turns speaking.
```json
{
  "dialogues": [
    {
      "role": "user",
      "content": "Now you are a fearch keywards generation tool based on Ubuntu, and will provide information to the user according to the following rules:\n1. Be able to extract keywords that may be helpful for searching related filenames or directory names based on the user-provided task description and return them in list form.\n2. The keywards can be a part of filename or a path, as long as it can be searched.\n3. If you cannot provide any information, just return the string '[]'.\n4. Ensure that the text you generate starts with the character '[' and ends with the character ']'."
    },
    {
      "role": "assistant",
      "content": "Okay, I understand."
    },
    {
      "role": "user",
      "content": "keywards related to the command {enter dir `tool_rsc`} are:"
    },
    {
      "role": "assistant",
      "content": "['tool_rsc']"
    },
    {
      "role": "user",
      "content": "keywards related to the command {Open my secret folder} are:"
    },
    {
      "role": "assistant",
      "content": "[]"
    },
    {
      "role": "user",
      "content": "keywards related to the command {create a new file `home.json` in my `miniconda3` installation directory} are:"
    },
    {
      "role": "assistant",
      "content": "['miniconda3']"
    }
  ]
}
```
</br>

## Extra tips
---------
- reset agent role 
  - If you want your agent to reset to the state it just initialized according to the JSON file or text description (which means making the agent forget all dialogs after initialization), you can simply call the `init_role()` function like this.
    ```python
    my_agent.init_role()
    ```
    If you don't want use `init_role()` so frequently, I highly recommand you use the parameter `remember_flag` of function `prompt_post()` flexibly .
