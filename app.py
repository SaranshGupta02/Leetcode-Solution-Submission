import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Streamlit UI setup
st.set_page_config(page_title="Leetcode Solution Generator", page_icon="📄", layout="centered")

st.title("📄 Leetcode Solution")
st.markdown("### ✨ Generate Leetcode Solution in Latex")

# Model initialization
llm = ChatOpenAI(model="o3-mini")


language = st.selectbox("🔹 Select Language", ["cpp", "python", "java", "javascript"])

# Input code
code = st.text_area(f"🔹 Enter {language.upper()} Code", height=200)
beats = st.number_input("Enter beats:", min_value=0, max_value=300, value=60)

# Optional numeric input for runtime
runtime = st.number_input("Enter runtime(ms):", min_value=0, max_value=1000, value=None, format="%d")

# Display formatted code and remove input area
if code:
    st.code(code, language=language)
if beats:
    st.write(beats)
if runtime:
    st.write(runtime)

def generate_response(llm,code,beats,runtime):
    template="""You have an immense knowledge of Data Structure and Algorithm . You solve all your DSA problems on leetcode.com . You have solved 3000+ problems in DSA
                You will be provided with a code and you have to prepare Solution in the proper format so that the user can submit the solution
                The format is :-
                # Intuition
<!-- Describe your first thoughts on how to solve this problem. -->

# Approach
<!-- Describe your approach to solving the problem. -->

# Complexity
- Time complexity:
<!-- Add your time complexity here, e.g. $$O(n)$$ -->

- Space complexity:
<!-- Add your space complexity here, e.g. $$O(n)$$ -->

# Code
```cpp []
    {code}
```
Requirements:
- Fill all the necessary field like Approach,Complexity as per the code given and return the response in the same latex format
- Add some Emojis/Latex Designing etc to improve the Submission Aesthetics
- Also write about the Beats and Runtime that the user beats {beats}% users and the runtime of code is {runtime}ms 
- Also provide Title for the submission . The Title is visible to Peoples before opening the solution So Title should be catchy, innovate , may be funny but i should be short
- Title Should tell people about our code like Its Complexity,Concepts used etc.
"""
    output_parser = StrOutputParser()
    prompt=ChatPromptTemplate.from_messages([
           ("system", template)
       ])
    
    chain= prompt | llm | output_parser
    
    response = chain.invoke({"code":code,"beats":beats,"runtime":runtime})
    st.code(response)
# Submit button
if st.button("Generate Solution🚀"):
    if code:
        generate_response(llm,code,beats,runtime)  # You will implement this function
    else:
        st.warning("Please fill in all required fields.")

# Footer
st.markdown("---")
st.markdown("🔹 *Powered by Saransh002❤️*")
