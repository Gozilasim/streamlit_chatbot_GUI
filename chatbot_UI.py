import streamlit as st
from datetime import datetime

import uuid
from database.db_function import save_message

# Function to read the CSS file and inject it into the Streamlit app
def inject_custom_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_message(message):
    copy_button = False
    
    if message["role"] == "user":
        div = f"""
            <div class="chat-row user-row row-reverse">
                <img src="app/static/profile.png" width=50 height =50>
                <div class="chat-content user-content">
                    <div>{message["content"]}</div>
            </div>
        """
        st.markdown(div, unsafe_allow_html=True)
        #copy_button = st.button("Copy", key=f"{message['role']}_copy_{message['timestamp']}")  # Unique key for each button

    elif message["role"] == "assistant":
        div = f"""
            <div class="chat-row assistant-row ">
                <img src="app/static/chatbot3.png" width=50 height = 50>
                <div class="chat-content assistant-content">
                    <div>{message["content"]}</div>

            </div>
        """
        st.markdown(div, unsafe_allow_html=True)


  


# Function to generate and store a unique session ID for each user
def get_session_id():
    if "session_id" not in st.session_state:
        # Generate a new unique session ID
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

session_id = get_session_id()




# GUI
def main():
    inject_custom_css("static/style.css")
    st.title("Fmea Bot🚨(●'◡'●)")

    with st.sidebar:
        st.write(f"Session ID: {session_id}")
        if st.button("New Chat"):
            # Reset session data and assign a new session ID
            st.session_state.clear()
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages=[]
            st.session_state.greetings = False
            print(f"session ID:  {session_id} ")
        
    if st.button("Help"):
        st.info("This is a chatbot interface. You can type your questions in the input box below and get responses. For more detailed instructions, refer to the user guide.")

    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.greetings = False

    if not st.session_state.greetings:
        intro = "Hey there! I'm FmeaBot, your assistant for finding the best solutions through Failure Modes and Effects Analysis (FMEA). Let's get started!"
        # div = f"""
        #     <div class="chat-row assistant-row ">
        #         <img src="app/static/chatbot3.png" width=50 height = 50>
        #         <div class="chat-content assistant-content">
        #             <div>{intro}</div>
        #     </div>
        # """

        st.session_state.messages.append({'role': 'assistant', 'content': intro})
        # st.markdown(div, unsafe_allow_html=True)
        st.session_state.greetings = True

    

    for message in st.session_state.messages:
        display_message(message)
        save_message(session_id, message["role"], message["content"])

    example_prompts = [
        "What is the detail of FC on Units contact by finger cot",
        "What is the detail of FC on Leadframe roller contact on glue",
        "What is the detail of FC on 20.1.2.2.1 Magazine Holder bar hit by hard object",
        "What is the detail of FC on Glue imprint on die after re-loading LF with attached good die",
        "What is the detail of FC on Magazine slot warpage",
        "Can u list down all the FE, FC, and FM that will happend on this package DSO and Power DSO to prevent these fialure happend again and agin?",
    ]

    example_prompts_help = example_prompts[:]
    
    button_cols = st.columns(3)
    button_cols_2 = st.columns(3)
    
    button_pressed = ""
    
    if button_cols[0].button(example_prompts[0], help=example_prompts_help[0]):
        button_pressed = example_prompts[0]
    elif button_cols[1].button(example_prompts[1], help=example_prompts_help[1]):
        button_pressed = example_prompts[1]
    elif button_cols[2].button(example_prompts[2], help=example_prompts_help[2]):
        button_pressed = example_prompts[2]
    
    elif button_cols_2[0].button(example_prompts[3], help=example_prompts_help[3]):
        button_pressed = example_prompts[3]
    elif button_cols_2[1].button(example_prompts[4], help=example_prompts_help[4]):
        button_pressed = example_prompts[4]
    elif button_cols_2[2].button(example_prompts[5], help=example_prompts_help[5]):
        button_pressed = example_prompts[5]
    
    if prompt := (st.chat_input("Type Your Prompt Here", max_chars=600) or button_pressed):   
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        st.session_state.messages.append({'role': 'user', 'content': prompt, 'timestamp': timestamp})
        div = f"""
            <div class="chat-row user-row row-reverse">
                <img src="app/static/profile.png" width=50 height =50>
                <div class="chat-content user-content">
                    <div>{prompt}</div>
            </div>
        """
        st.markdown(div, unsafe_allow_html=True)
   
        
        with st.spinner('Generating response...'):
            response = "hihi"

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        st.session_state.messages.append({'role': 'assistant', 'content': response, 'timestamp': timestamp})
        div = f"""
            <div class="chat-row assistant-row ">
                <img src="app/static/chatbot3.png" width=50 height = 50>
                <div class="chat-content assistant-content">
                    <div>{response}</div>

            </div>
        """
        st.markdown(div, unsafe_allow_html=True)

        save_message(session_id, message["role"], message["content"])
    

if __name__ == "__main__":
    main()
