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
beats=0
runtime=0
# Input code
code = st.text_area(f"🔹 Enter {language.upper()} Code", height=200)
beats = st.number_input("Enter Beats(%):", min_value=0, max_value=300,value=None)

# Optional numeric input for runtime
runtime = st.number_input("Enter runtime(ms):", min_value=0, max_value=1000, value=None, format="%d")


# Display formatted code and remove input area
if code:
    st.code(code, language=language)

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
- Can Also mention about the Beats and Runtime that the user beats {beats}% users and the runtime of code is {runtime}ms 
- Mention about the Beats and Runtime in Title or Approach but dont Explicitly mention beats and runtime
- Also provide Title for the submission . The Title is visible to Peoples before opening the solution So Title should be catchy, innovate , may be funny but i should be short
- Title Should tell people about our code like Its Complexity,Concepts used etc.
- at last Give a single line Funny/Roasting Complement to the user about the code/coding/leetcode/Dsa Competetion etc. motivating the user to solve more problem
- Remember the Complement should be either Funny/Roasting it should not be serious and complement should be in proper format : Complement : [Complement]
"""
    output_parser = StrOutputParser()
    prompt=ChatPromptTemplate.from_messages([
           ("system", template)
       ])
    
    chain= prompt | llm | output_parser
    
    response = chain.invoke({"code":code,"beats":beats,"runtime":runtime})

    response,complement = parse_response(response)
    st.code(response)
    st.success(complement)  # Green box (success message)
    st.warning(complement)  # Yellow box (warning)
    st.error(complement)    # Red box (error message)
    st.info(complement) 

def parse_response(response):
    lines = response.split("\n")
    response1 = ""
    complement = ""
    
    for line in lines:
        if line.strip().startswith("Complement"):
            complement = line.strip()[len("Complement:"):].strip()
            if complement.startswith(":"):
                complement = complement[1:]
            if complement.startswith("[") and complement.endswith("]"):
                complement = complement[1:-1]  # Remove first and last character
        else:
            response1 += line + "\n"
    
    return response1.strip(), complement  # Remove extra whitespace

# Submit button
if st.button("Generate Solution🚀"):
    if code:
        generate_response(llm,code,beats,runtime)  # You will implement this function
    else:
        st.warning("Please fill in all required fields.")

# Footer
st.markdown("---")
st.markdown("🔹 *Powered by Saransh002❤️*")
