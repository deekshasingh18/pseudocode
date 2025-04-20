# pseudo2code_app.py

import streamlit as st

# Basic rule-based pseudo code parser (MVP version)
def parse_pseudocode(pseudo, language):
    lines = pseudo.strip().split('\n')
    code_lines = []

    for line in lines:
        line = line.strip()

        if line.lower().startswith("set"):
            # Example: Set sum = 0
            parts = line.split("=")
            if len(parts) == 2:
                var = parts[0].replace("Set", "").strip()
                val = parts[1].strip()
                if language == "Python":
                    code_lines.append(f"{var} = {val}")
                elif language == "C++" or language == "Java":
                    code_lines.append(f"int {var} = {val};")

        elif line.lower().startswith("for"):
            # Example: For i from 1 to 5
            tokens = line.split()
            if "from" in tokens and "to" in tokens:
                var = tokens[1]
                start = tokens[tokens.index("from") + 1]
                end = tokens[tokens.index("to") + 1]

                if language == "Python":
                    code_lines.append(f"for {var} in range({start}, {int(end)+1}):")
                elif language == "C++":
                    code_lines.append(f"for (int {var} = {start}; {var} <= {end}; {var}++) {{")
                elif language == "Java":
                    code_lines.append(f"for (int {var} = {start}; {var} <= {end}; {var}++) {{")

        elif line.lower().startswith("print"):
            val = line.replace("Print", "").strip()
            if language == "Python":
                code_lines.append(f"print({val})")
            elif language == "C++":
                code_lines.append(f"cout << {val} << endl;")
            elif language == "Java":
                code_lines.append(f"System.out.println({val});")

        elif line.lower() == "end":
            if language in ["C++", "Java"]:
                code_lines.append("}")

        else:
            code_lines.append(f"# Unrecognized: {line}")

    return "\n".join(code_lines)

# Streamlit UI
st.set_page_config(page_title="Pseudo2Code Generator", layout="centered")
st.title("🤖 Pseudo2Code Generator")
st.markdown("Generate code from structured pseudo code in Python, Java, or C++.")

# Input area
pseudo_code = st.text_area("Enter your Pseudo Code:", height=200)
language = st.selectbox("Select Target Language:", ["Python", "Java", "C++"])

# Generate button
if st.button("Generate Code"):
    if pseudo_code.strip():
        output_code = parse_pseudocode(pseudo_code, language)
        st.code(output_code, language.lower())
    else:
        st.warning("Please enter some pseudo code to proceed.")

