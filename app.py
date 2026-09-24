from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from legalease import export_document_to_docx, export_document_to_pdf, export_document_to_txt, generate_document

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown(
    """
    <style>
    .main { background: linear-gradient(135deg, #f7f9fc 0%, #eef4ff 100%); }
    div[data-testid="stForm"] { background: white; border-radius: 12px; padding: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚖️ LegalEase AI-Powered Legal Document Generator")
st.caption("Generate polished legal documents for business, hiring, and commercial relationships.")

with st.sidebar:
    st.header("Workflow")
    st.markdown("1. Select a document type\n2. Enter party and contract details\n3. Generate the draft\n4. Brand and export")
    st.info("Tip: If AI is not configured, the app uses a structured legal template fallback.")
    st.caption(f"AI mode: {'Enabled' if os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY') else 'Fallback template'}")

    company_name = st.text_input("Company Name", "Acme Legal Solutions")
    uploaded_logo = st.file_uploader("Upload logo", type=["png", "jpg", "jpeg"])
    if uploaded_logo is not None:
        output_dir = Path("generated")
        output_dir.mkdir(exist_ok=True)
        logo_path = output_dir / uploaded_logo.name
        logo_path.write_bytes(uploaded_logo.getvalue())
        st.session_state["logo_path"] = str(logo_path)
        st.success(f"Logo saved: {logo_path}")
    elif "logo_path" in st.session_state:
        st.session_state["logo_path"] = st.session_state["logo_path"]

with st.form("legal_form"):
    col1, col2 = st.columns(2)
    with col1:
        document_type = st.selectbox(
            "Document Type",
            ["Service Agreement", "NDA", "Employment Agreement", "Consulting Agreement"],
        )
        party_name = st.text_input("Party 1 / Client Name", "Acme Corp")
        other_party_name = st.text_input("Party 2 / Counterparty Name", "Beta LLC")
        role = st.text_input("Role or Title", "Senior Product Manager")
        jurisdiction = st.text_input("Jurisdiction", "Delaware, USA")

    with col2:
        effective_date = st.date_input("Effective Date")
        deliverables = st.text_area(
            "Deliverables or Scope",
            "Software development, implementation support, and performance monitoring services.",
            height=120,
        )
        purpose = st.text_area(
            "Purpose",
            "The agreement is intended to define the rights, responsibilities, and obligations of the parties in connection with the commercial relationship.",
            height=120,
        )
        additional_terms = st.text_area(
            "Additional Terms",
            "Confidentiality, dispute resolution, governing law, and mutual good-faith cooperation.",
            height=120,
        )

    submitted = st.form_submit_button("Generate Document", use_container_width=True)

if submitted:
    with st.spinner("Generating your legal document..."):
        payload = {
            "document_type": document_type,
            "party_name": party_name,
            "other_party_name": other_party_name,
            "role": role,
            "jurisdiction": jurisdiction,
            "effective_date": str(effective_date),
            "deliverables": deliverables,
            "purpose": purpose,
            "additional_terms": additional_terms,
        }
        st.session_state["document_text"] = generate_document(payload)
        st.session_state["company_name"] = company_name

if "document_text" in st.session_state:
    st.subheader("Generated Draft")
    document_text = st.session_state["document_text"]
    edited_text = st.text_area("Document Preview", document_text, height=500)
    if st.button("Save Edits", use_container_width=True):
        st.session_state["document_text"] = edited_text
        st.success("Document edits saved.")

    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    with col_a:
        if st.button("Copy to Clipboard", use_container_width=True):
            st.code(edited_text, language="text")
    with col_b:
        output_dir = Path("generated")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "legal_document.pdf"
        if st.button("Export as PDF", use_container_width=True):
            export_document_to_pdf(
                edited_text,
                str(output_path),
                company_name=st.session_state.get("company_name", "LegalEase"),
                logo_path=st.session_state.get("logo_path"),
            )
            st.success(f"PDF saved to: {output_path}")
    with col_c:
        output_docx_path = output_dir / "legal_document.docx"
        if st.button("Export as DOCX", use_container_width=True):
            export_document_to_docx(
                edited_text,
                str(output_docx_path),
                company_name=st.session_state.get("company_name", "LegalEase"),
                logo_path=st.session_state.get("logo_path"),
            )
            st.success(f"DOCX saved to: {output_docx_path}")
    with col_d:
        output_txt_path = output_dir / "legal_document.txt"
        if st.button("Export as TXT", use_container_width=True):
            export_document_to_txt(edited_text, str(output_txt_path))
            st.success(f"Text file saved to: {output_txt_path}")
    with col_e:
        if st.button("Generate New Draft", use_container_width=True):
            st.session_state.pop("document_text", None)

    pdf_path = output_dir / "legal_document.pdf"
    docx_path = output_dir / "legal_document.docx"
    txt_path = output_dir / "legal_document.txt"
    if pdf_path.exists():
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name="legal_document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    if docx_path.exists():
        with open(docx_path, "rb") as file:
            st.download_button(
                label="Download DOCX",
                data=file,
                file_name="legal_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
    if txt_path.exists():
        with open(txt_path, "rb") as file:
            st.download_button(
                label="Download TXT",
                data=file,
                file_name="legal_document.txt",
                mime="text/plain",
                use_container_width=True,
            )

st.markdown("---")
st.caption("LegalEase is designed for drafting and export assistance; legal review is still recommended before use.")
