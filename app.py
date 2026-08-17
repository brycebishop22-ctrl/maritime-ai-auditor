import streamlit as st
from pypdf import PdfReader
from openai import OpenAI

st.set_page_config(page_title="AI Maritime Logistics Auditor", layout="wide", page_icon="⚓")
st.title("⚓ AI Maritime Logistics & D&D Auditor")
st.subheader("Instantly catch document discrepancies and demurrage fee risks.")

# Secure API Key Entry
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
st.sidebar.markdown("---")
st.sidebar.info("Upload a PDF Bill of Lading (BoL) to run an instant compliance and financial risk audit.")

uploaded_file = st.file_uploader("Drag and drop your Bill of Lading (PDF)", type=["pdf"])

if uploaded_file:
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar to run the analysis.")
    else:
        with st.spinner("AI is auditing documentation and checking port timelines..."):
            try:
                # Extract text from the PDF
                reader = PdfReader(uploaded_file)
                raw_text = ""
                for page in reader.pages:
                    raw_text += page.extract_text() or ""

                # Connect to OpenAI
                client = OpenAI(api_key=api_key)

                prompt = f"""
                You are an expert maritime logistics auditor and port clerk. Analyze this raw text extracted from a Bill of Lading:

                {raw_text}

                Provide a structured report using clean markdown headers. You must include:
                1. ### 📦 Extracted Ship Data (Container ID, Carrier Name, Vessel/Voyage Number, Port of Discharge)
                2. ### 🚨 Demurrage & Detention (D&D) Risk Assessment (Rate it Low, Medium, or High. Give a 1-sentence reason based on potential timeline delays or missing information).
                3. ### ❌ Documentation Discrepancies & Compliance Errors (List any missing fields, formatting errors, or mismatched details that could trigger a customs hold).
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                )

                st.success("Audit Complete!")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
