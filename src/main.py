import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser



load_dotenv()
def main():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    
    st.set_page_config(
        page_title="streamlit-chat-bot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.title("Welcome to the Streamlit Chat Bot!")
    
    #  get responses from the chat model
    def get_chat_response(user_input, chat_history):
        template = """
        You are a helpful assistant. 
        Provide concise and relevant answers to the user's questions based on the conversation history.
        Chat history:{chat_history}
        User input: {user_input}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatOpenAI(streaming=True, api_key=os.getenv("OPENAI_API_KEY"))
        
        chain = prompt | llm | StrOutputParser()
        
        response = chain.stream({
            "user_input": user_input,
            "chat_history": chat_history
        })
        return response
    
    
    # conversation container
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:
            with st.chat_message('assistant'):
                st.markdown(message.content)
    
    #  user input
    user_query = st.chat_input("Your message...", key="user_input")
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            response =st.write_stream(get_chat_response(
                user_input=user_query,
                chat_history=st.session_state.chat_history
            ))
            
        st.session_state.chat_history.append(AIMessage(content=response))




if __name__ == "__main__":
    main()