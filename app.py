import streamlit as st
import os
from src.utils.rfp_runner import RFPRunner
from datetime import datetime
import tempfile
from helpers import convert_md_to_docx
from dotenv import load_dotenv
load_dotenv(override=True)

st.set_page_config(page_title="AI RFP Generator", page_icon="📄", layout="wide")
st.title("📄 AI-Powered RFP Generation System")

st.markdown("""
<style>
/* Make sidebar wider */
[data-testid="stSidebar"] {
    min-width: 475px;
    max-width: 550px;
    width: 475px;
}

/* Expand main container padding */
.main .block-container {
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    Welcome to the **AI-Powered RFP Generator**.  
    This application uses intelligent agents to generate professional Request for Proposal (RFP) 
    documents for enterprise software and data platform projects.

    Upload your project details in JSON format, choose a configuration file, and the system will do the rest!
    """)
    
    st.markdown("### 🧠 Meet the Agents")
    st.markdown("""
    | 🧑‍💼 **Agent Role**        | 🛠️ **Responsibility**                                   |
    |---------------------------|-----------------------------------------------------------|
    | 🧾 Requirements Analyst    | Extracts business needs and constraints                   |
    | 🏗 Technical Architect     | Designs high-level architecture and tech stack            |
    | 💼 Business Analyst        | Aligns project with strategic goals                       |
    | 🛡 Compliance Officer      | Ensures regulatory requirements are addressed             |
    | 💰 Cost Estimator          | Projects cost based on benchmarks and scope               |
    | ✍️ RFP Writer              | Synthesizes all information into the final document       |
    """)

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712047.png", width=160)
    
    st.markdown("### 🔁 Generation Process")
    st.markdown("""
    1. Upload your project input file  
    2. Select optional configuration YAML file  
    3. Click **Generate RFP**  
    4. Agents collaborate and write the proposal  
    5. Download the results in Markdown and Word Document
    """)
    
with st.sidebar:
    st.header("📁 Upload Files")
    uploaded_input = st.file_uploader("Upload Project JSON", type="json", key="project_upload")
    uploaded_config = st.file_uploader("Upload Config YAML", type=["yaml", "yml"], key="config_upload")
    output_dir = st.text_input("Output Directory", value="outputs/generated_rfps")
    run_button = st.button("🚀 Generate RFP")
    
    st.markdown("### 🏗️ System Architecture")
    st.markdown("""
    **Modular Multi-Agent System Architecture**

    🔹 **Input Layer** – Handles uploaded project and config files

    🔹 **Agent Orchestrator (CrewAI)**
    - 🧾 Requirements Analyst
    - 🏗 Technical Architect
    - 💼 Business Analyst
    - 🛡 Compliance Officer
    - 💰 Cost Estimator
    - ✍️ RFP Writer

    🔹 **Output Layer** – Generates Markdown and Word documents
    """)
    
    if os.getenv('OPENAI_API_KEY'):
        st.success("✅ OpenAI API connected")
    else:
        st.error("❌ OpenAI API key missing")

st.markdown("### 🔄 Agent Interaction Flow")
st.graphviz_chart("""
    digraph {
      rankdir=LR
      node [shape=box, style="filled", color="#e0f7fa", fontname="Arial", fontsize=20, width=2, height=1.10]

      Input [label="📤 Input Layer\n(Project JSON + Config)"]
      ReqAnalyst [label="🧾 Requirements Analyst"]
      TechArchitect [label="🏗 Technical Architect"]
      BusinessAnalyst [label="💼 Business Analyst"]
      ComplianceOfficer [label="🛡 Compliance Officer"]
      CostEstimator [label="💰 Cost Estimator"]
      RFPWriter [label="✍️ RFP Writer"]
      Output [label="📄 RFP Output\n(Markdown + Word Doc)"]

      Input -> ReqAnalyst
      ReqAnalyst -> TechArchitect
      ReqAnalyst -> BusinessAnalyst
      ReqAnalyst -> ComplianceOfficer
      TechArchitect -> CostEstimator
      BusinessAnalyst -> CostEstimator
      ComplianceOfficer -> RFPWriter
      CostEstimator -> RFPWriter
      RFPWriter -> Output
    }
s""")

if run_button and uploaded_input:
    try:
        with st.spinner("Running AI agents and generating RFP..."):
            # Create temporary file for input JSON
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='wb') as tmp_input:
                tmp_input.write(uploaded_input.read())
                input_path = tmp_input.name

            # Optional config file
            if uploaded_config:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", mode='wb') as tmp_config:
                    tmp_config.write(uploaded_config.read())
                    config_path = tmp_config.name
            else:
                config_path = "config.yaml"

            summary = RFPRunner.run_rfp_pipeline(
                input_json_path=input_path,
                config_path=config_path,
                output_dir=output_dir,
                verbose=True
            )

            st.success("✅ RFP generated successfully!")
            st.markdown(f"**📄 Output File:** `{summary['output_file']}`")
            st.markdown(f"**📊 Project:** `{summary['project_name']}`")
            st.markdown(f"**🏢 Client:** `{summary['client']}`")
            st.markdown(f"**🏭 Industry:** `{summary['industry']}`")
            st.markdown(f"**📁 Type:** `{summary['project_type']}`")
            st.markdown(f"**💰 Budget:** `{summary['budget']}`")

            # Download buttons
            md_file_path = summary['output_file']
            docx_file_path = md_file_path.replace(".md", ".docx")
            
            custom_css = """
            <style>
            h1, h2, h3 {
                color: #0E1117;
                border-bottom: 1px solid #CCC;
                padding-bottom: 4px;
            }
            p {
                font-size: 15px;
                line-height: 1.6;
            }
            ul {
                padding-left: 20px;
            }
            </style>
            """
            
            # Preview the generated RFP
            st.markdown("---")
            st.markdown("### 📄 Generated RFP Preview")

            # Load the Markdown content
            with open(md_file_path, 'r', encoding='utf-8') as f:
                rfp_markdown = f.read()
                
            st.markdown(custom_css, unsafe_allow_html=True)

            with open(md_file_path, 'r', encoding='utf-8') as f:
                st.download_button("⬇️ Download Markdown", data=f.read(), file_name=os.path.basename(md_file_path), mime="text/markdown")
                
            # Convert to DOCX if not exists
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
                if not os.path.exists(docx_file_path):
                    convert_md_to_docx(md_content, docx_file_path)
                
            # Show Word download button
            if os.path.exists(docx_file_path):
                with open(docx_file_path, "rb") as f:
                    st.download_button(
                        label="📃 Download Word",
                        data=f.read(),
                        file_name=os.path.basename(docx_file_path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    
            # Optional: Clean up temporary files
            os.remove(input_path)
            if uploaded_config:
                os.remove(config_path)

    except Exception as e:
        st.error(f"❌ Failed to generate RFP: {str(e)}")
