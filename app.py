
import os
from pathlib import Path

import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# LOAD API KEY
# --------------------------------------------------

load_dotenv(Path(__file__).resolve().parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


# --------------------------------------------------
# APP TITLE
# --------------------------------------------------

st.title("PDF Intelligence")
st.write("Upload a PDF and analyze its content.")


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

pdf = st.file_uploader("Upload PDF", type="pdf")


if pdf:
    try:
        reader = PdfReader(pdf)

        text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )

        char_count = len(text)

        st.info(f"PDF contains {char_count:,} characters.")

        MAX_CHARACTERS = 20000

        if char_count > MAX_CHARACTERS:
            st.warning(
                "This PDF is large. Processing the entire document "
                "may take longer or exceed the AI model's input limit."
            )

        if not text.strip():
            st.warning("No readable text found in this PDF.")

        else:
            st.success("PDF uploaded successfully.")

            # --------------------------------------------------
            # ANALYSIS MODE
            # --------------------------------------------------

            mode = st.radio(
                "Choose an option",
                [
                    "Ask a question",
                    "Summarize PDF",
                    "Extract Key Points"
                ],
                horizontal=True
            )

            question = ""
            num_points = 5

            if mode == "Ask a question":
                question = st.text_input(
                    "Ask a question about the PDF"
                )

            if mode == "Extract Key Points":
                num_points = st.slider(
                    "Number of key points",
                    min_value=3,
                    max_value=15,
                    value=5
                )

            # --------------------------------------------------
            # AI SETTINGS
            # --------------------------------------------------

            with st.expander("AI Settings"):

                thinking_level = st.selectbox(
                    "AI Thinking Level",
                    options=["low", "medium", "high"],
                    index=1,
                    help=(
                        "Controls how much reasoning effort the AI uses. "
                        "Higher levels may take longer."
                    )
                )

                max_output_tokens = st.slider(
                    "Maximum final output tokens",
                    min_value=256,
                    max_value=4096,
                    value=2048,
                    step=256,
                    help="Sets the maximum length of the final AI response."
                )

            # --------------------------------------------------
            # RUN ANALYSIS
            # --------------------------------------------------

            if st.button("Run Analysis"):

                if not client:
                    st.error(
                        "API key not found. Check your .env file."
                    )

                elif mode == "Ask a question" and not question.strip():
                    st.warning("Please enter a question.")

                else:

                    # --------------------------------------------------
                    # STAGE 2 PROMPTS
                    # --------------------------------------------------

                    if mode == "Summarize PDF":

                        prompt = (
                            "You are an expert document analyst.\n"
                            "Write a clear and accurate summary based "
                            "only on the extracted findings.\n"
                            "Include the main topic, important points, "
                            "and conclusion if present.\n"
                            "Use simple language. Do not invent facts."
                        )

                    elif mode == "Extract Key Points":

                        prompt = (
                            "You are an expert document analyst.\n\n"

                            "Example input:\n"
                            "The school library added 500 new books "
                            "in September. Students can borrow up to "
                            "three books at a time.\n\n"

                            "Example output:\n"
                            "1. The library added 500 new books "
                            "in September.\n"
                            "2. Students can borrow up to three "
                            "books at a time.\n\n"

                            "Now analyze the extracted findings.\n"
                            f"Extract exactly {num_points} important "
                            "key points.\n"
                            "Use a numbered list.\n"
                            "Keep each point concise and supported "
                            "by the findings."
                        )

                    else:

                        prompt = (
                            "You are a PDF question-answering assistant.\n"
                            "Answer the user's question using only "
                            "the extracted findings.\n"
                            "If the answer is not present, say: "
                            "'The answer is not available in the "
                            "provided document.'\n"
                            "Do not guess or use outside knowledge.\n"
                            "Give a clear and concise answer.\n"
                            f"Question: {question}"
                        )

                    try:

                        # --------------------------------------------------
                        # STAGE 1: STRUCTURED DOCUMENT ANALYSIS
                        # --------------------------------------------------

                        with st.spinner(
                            "Stage 1: Extracting facts and topics..."
                        ):

                            stage1 = client.interactions.create(
                                model="gemini-3.8-flash",

                                input=(
                                    "You are a document analysis assistant.\n\n"

                                    "Analyze the document using this "
                                    "structured workflow:\n\n"

                                    "Step 1: Identify the main topics "
                                    "and purpose of the document.\n"

                                    "Step 2: Extract important facts, "
                                    "dates, names, and entities.\n"

                                    "Step 3: Group related facts into "
                                    "clear categories.\n"

                                    "Step 4: Check that each finding "
                                    "is supported by the document.\n"

                                    "Step 5: Prepare a concise, "
                                    "organized set of findings.\n\n"

                                    "Return the results using these "
                                    "sections:\n"
                                    "1. Main Topics\n"
                                    "2. Important Facts\n"
                                    "3. Dates and Entities\n"
                                    "4. Key Findings\n"
                                    "5. Conclusion\n\n"

                                    "Do not return headings without "
                                    "information.\n"
                                    "If a section has no relevant "
                                    "information, write 'Not mentioned'.\n"
                                    "Do not invent facts.\n\n"

                                    f"PDF content:\n{text}"
                                ),

                                generation_config={
                                    "thinking_level": thinking_level,
                                    "max_output_tokens": 2048
                                },
                            )

                        findings = stage1.output_text or ""

                        # --------------------------------------------------
                        # SHOW STAGE 1 FINDINGS
                        # --------------------------------------------------

                        with st.expander(
                            "View Stage 1: Extracted Findings"
                        ):
                            st.write(
                                findings or "No findings returned."
                            )

                        if not findings.strip():

                            st.error(
                                "Stage 1 did not return any findings. "
                                "Please try again."
                            )

                        else:

                            # --------------------------------------------------
                            # STAGE 2: GENERATE FINAL RESULT
                            # --------------------------------------------------

                            with st.spinner(
                                "Stage 2: Generating final result..."
                            ):

                                response = client.interactions.create(
                                    model="gemini-3.8-flash",

                                    input=(
                                        f"{prompt}\n\n"

                                        "Use the following extracted "
                                        "findings to produce the final "
                                        "answer.\n"

                                        "Use only information supported "
                                        "by the findings.\n\n"

                                        f"Extracted findings:\n{findings}"
                                    ),

                                    generation_config={
                                        "thinking_level": thinking_level,
                                        "max_output_tokens": max_output_tokens
                                    },
                                )

                            # --------------------------------------------------
                            # DISPLAY FINAL RESULT
                            # --------------------------------------------------

                            result = response.output_text or ""

                            st.subheader("Result")

                            if result.strip():

                                st.markdown(result)

                                # --------------------------------------------------
                                # DOWNLOAD RESULT
                                # --------------------------------------------------

                                st.download_button(
                                    label="Download Result",
                                    data=result,
                                    file_name="pdf_analysis_result.txt",
                                    mime="text/plain"
                                )

                            else:

                                st.warning(
                                    "The AI did not return a result."
                                )


                    except Exception as e:

                        error_message = str(e).lower()

                        if (
                                "429" in error_message
                                or "rate limit" in error_message
                                or "quota" in error_message
                        ):

                            st.error(

                                "Gemini API rate limit reached. "

                                "Please wait and try again later."

                            )


                        elif "timeout" in error_message or "timed out" in error_message:

                            st.error(

                                "The request took too long. "

                                "Please try again with a smaller PDF."

                            )


                        elif "503" in error_message or "unavailable" in error_message:

                            st.error(

                                "The AI service is temporarily unavailable. "

                                "Please try again later."

                            )


                        else:

                            st.error(f"Gemini API error: {e}")

    except Exception as e:

        st.error(f"Could not read PDF: {e}")
