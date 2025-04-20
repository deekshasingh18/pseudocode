import streamlit as st
import openai

# Page configuration
st.set_page_config(page_title="Pseudo2Code (with Explain)", layout="centered")

st.title("🤖 Pseudo2Code + Code Explainer")
st.markdown("Convert any human-readable pseudo code into real code & understand it!")

# Step 1: API key
openai.api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

# Step 2: Pseudo code input
pseudo_code = st.text_area("📝 Enter your Pseudo Code:", height=250, placeholder="e.g.\nfunction fib(n):\n  if n is 0 or 1:\n    return n\n  else:\n    return fib(n-1) + fib(n-2)")

# Step 3: Language selection
language = st.selectbox("🌐 Select Output Language", ["Python", "C++", "Java"])

# Step 4: Button to generate code
generate_button = st.button("🚀 Generate Code")
explain_button = st.button("💬 Explain Code")

# Global code variable
if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

# Step 5: Generate Code
if generate_button:
    if not openai.api_key:
        st.error("Please enter your OpenAI API key.")
    elif not pseudo_code.strip():
        st.warning("Please enter some pseudo code.")
    else:
        with st.spinner("Generating Code..."):
            prompt = f"""Convert the following pseudocode to {language}:

{pseudo_code}

Please write clean and well-structured {language} code.
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )

                code = response['choices'][0]['message']['content']
                st.session_state.generated_code = code
                st.success("✅ Code Generated Successfully!")
                st.code(code, language=language.lower())

            except Exception as e:
                st.error(f"❌ Error: {e}")

# Step 6: Explain Code
if explain_button:
    if not st.session_state.generated_code.strip():
        st.warning("Generate the code first to get an explanation.")
    else:
        with st.spinner("Explaining Code..."):
            explain_prompt = f"""Explain the following {language} code in simple language for a beginner:

{st.session_state.generated_code}
"""

            try:
                explain_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": explain_prompt}],
                    temperature=0.3
                )

                explanation = explain_response['choices'][0]['message']['content']
                st.success("🧠 Code Explanation:")
                st.markdown(explanation)

            except Exception as e:
                st.error(f"❌ Error: {e}")
