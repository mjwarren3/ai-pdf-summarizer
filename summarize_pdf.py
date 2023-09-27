import os
import config
os.environ['OPENAI_API_KEY'] = config.API_KEY

import gradio as gr
from langchain import OpenAI, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader

llm = OpenAI(temperature=0)

def summarize_pdf(pdf_file_path, custom_prompt=""):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary=chain.run(docs)
    if custom_prompt!="":
        prompt_template = custom_prompt + """
        {text}
        SUMMARY:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=PROMPT, combine_prompt=PROMPT)
        custom_summary = chain({"input_documents": docs}, return_only_outputs=True)["output_text"]
    else:
        custom_summary = ""
    return summary, custom_summary

def main():
    input_pdf_path = gr.inputs.Textbox(label="Enter the PDF file path")
    input_custom_prompt = gr.inputs.Textbox(label="Enter your custom prompt")
    output_summary = gr.outputs.Textbox(label="Summary")
    output_custom_summary = gr.outputs.Textbox(label="Custom Summary")

    iface = gr.Interface(
        fn=summarize_pdf,
        inputs=[input_pdf_path, input_custom_prompt],
        outputs=[output_summary, output_custom_summary],
        title="AI PDF Summarizer",
    )

    iface.launch()

if __name__ == "__main__":
    main()