import streamlit as st
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import cv2
import numpy as np
from models import Invoice 
from pdf_converter import pdf_image_text, pdf_parser_text
import tempfile

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", key="api_key", type="password", value="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")
    model = st.text_input("Model Id", key="model", value="llama-3.1-8b-instant")
    "[![source in GitHub ](https://github.com/codespaces/badge.svg)](https://github.com/achreftlili/ovrsea-test)"

st.title("📝 Invoice File Extractor with Groq, LangChain, openCV")

#Get the uploaded file
uploaded_file = st.file_uploader("Upload an invoice", type=("pdf"))
uploaded_file_path = ""
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        uploaded_file_path = temp_file.name

#Create the output parser based on the Invoice Model
output_parser = JsonOutputParser(pydantic_object=Invoice)


#Create the prompt
prompt = PromptTemplate(
    template=(
        """
        You are an intelligent assistant specialized in extracting structured data from unstructured text. Your task is to extract specific information from an invoice, distinguishing between line items and VAT lines. Respond only with the extracted data in valid JSON format according to the schema below. Use the chain of thought reasoning to break down the task into steps.
        {format_instructions}
        Guidelines:
            By default, the quantity is 1 if not specified.
            Exclude any VAT and VAT-related clauses from Line Items.
        Chain of Thought Reasoning:
            Extract Invoice Metadata:
                Extract and store the invoice number, invoice date, due date, total amount, currency, and supplier name.
                Identify Line Items:
                Identify sections of the text that list line items. Generally, these sections will include product descriptions, quantities, unit prices, and line totals.
            Filter VAT Lines:
                Exclude any lines mentioning VAT or related clauses from the identified line items.
            Format Line Items:
                For each valid line item, extract the description, quantity, unit price, and line total. If the quantity is not specified, default it to 1.
            Compile JSON Output:
                Organize the extracted information into the predefined JSON schema.
        Context:
            Here is the invoice text from the parser: {pdf_parser_text}
            If the parser text isn’t sufficient, use the invoice text from image to text: {pdf_image_text}
        Use this structured approach to accurately extract and format the required data. """
    ),
    input_variable=["pdf_parser_text","pdf_image_text"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
)

if uploaded_file and not groq_api_key and not model:
    st.info("Please add your Groq API Key and Model ID to continue.")

if uploaded_file and groq_api_key and model:
    
    st.write("### Answer")
    #Create the LLM instance with Groq
    llm = ChatGroq(groq_api_key=groq_api_key, model_name=model)
    chain = prompt | llm | output_parser
        
    try:
        #Invoke our chain to get the final result  
        response = chain.invoke({"pdf_parser_text": pdf_parser_text(uploaded_file_path),"pdf_image_text": pdf_image_text(uploaded_file_path)})
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
