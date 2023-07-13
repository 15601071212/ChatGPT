# ChatGPT-learning
如何调用GPT-3 API通过输入的提示词prompt读取一段文本并输出一句话的摘要。
- 调用GPT-3 API的源代码
```python
#GPT-3 API 演示程序Python代码
import openai
import os

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""

prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""

response = get_completion(prompt)
print(response)
```
- 程序运行输出结果：
```python
The text emphasizes the importance of providing clear and specific instructions to guide a model towards the desired output,
suggesting that longer prompts can often provide more clarity and context for the model,
resulting in more detailed and relevant responses.
```

