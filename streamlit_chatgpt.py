import streamlit as st
import os
import openai 
import json

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model,temperature):
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

st.set_page_config(
        page_title="ChatGPT 你问我答",
        page_icon="",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'About': "### design by Ryan Liu 2024.01.13"
        }
    )

st.sidebar.title('ChatGPT 你问我答')
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    '选择模型名称',
    ('gpt-4-turbo-preview','gpt-4-1106-preview','gpt-4-vision-preview','gpt-4-32k')
)
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    '选择随机性指数',
    0.0, 2.0, 0.2
)

model = add_selectbox
temperature = add_slider



# Get conversation history from session state
conversation_history = st.session_state.get('conversation_history', [])

# Display the conversation history
st.markdown("""
    <style>
    .reportview-container .markdown-text-container {
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)
for conv in conversation_history:
    with st.chat_message("human"):
        st.markdown(conv["question"])
    with st.chat_message("ai"):
        st.markdown(conv["answer"])
    

if len(conversation_history)==0:
    question_example="你是谁，能帮我干什么？"
    answer_example='''
我是一个人工智能助手，可以帮助你解答各种问题，提供信息，以及协助你完成各种任务。我的功能包括但不限于：

回答一般性问题：
1. 比如关于科学、历史、文化、技术等领域的问题。
2. 提供实用信息：如天气预报、新闻更新、食谱、健康建议等。
3. 协助学习：帮助你理解复杂的概念，提供学习资源和策略。
4. 语言翻译：帮助你理解或翻译不同语言的文字。
5. 生活助手：提醒你日程安排，帮助你管理待办事项。
6. 娱乐推荐：推荐电影、音乐、书籍等娱乐内容。
7. 技术支持：提供基本的电脑和软件使用帮助。

请注意，我的能力有限，我提供的信息和帮助基于我被编程的知识和数据。如果你有任何问题，只需问我，我会尽我所能提供帮助。
    '''
    with st.chat_message("human"):
            st.markdown(question_example)
    with st.chat_message("ai"):
            st.markdown(answer_example)
 


question = st.chat_input("请输入你的问题，换行请使用Shift+Enter")
answer = ''
if question:
    # if len(q_and_a_history)==0:
    #     q_and_a_history.append(f"User: {question}")
    #     answer = get_completion(question, model,temperature)
    #     q_and_a_history.append(f"{answer}")
    # else:

    if len(conversation_history)==0:
        answer = get_completion(question, model,temperature)
    else:
        q_and_a_history=[]
        for conv in conversation_history:
            q_and_a_history.append(conv['question'])
            q_and_a_history.append(conv['answer'])
        q_and_a_history.append(question)
        prompt='\n'.join(q_and_a_history)
        answer = get_completion(prompt, model,temperature)
    # Append the new conversation to the history
    conversation_history.append({'question': question, 'answer': answer})
    #conversation_history.append({'question': question, 'answer': '%s:%s' % (answer1,answer2)})
    # Update the session state with the new conversation history
    st.session_state.conversation_history = conversation_history
    # Reset the temporary variable for the input value
    st.session_state.input_value = ''
    # Rerun the app to update the conversation display
    st.rerun()
