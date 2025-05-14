import gradio as gr
import requests
from bs4 import BeautifulSoup
import groq
import os
from dotenv import load_dotenv
from google.colab import userdata

# Load environment variables
load_dotenv()
# Initialize API keys from Colab secrets
groq_api_key   = os.environ["GROQ_API_KEY"]   = userdata.get("GROQ_API_KEY")
#print(groq_api_key)
# Initialize clients
groq_client = groq.Client(api_key=groq_api_key)
def summarize_text(text, max_length=4000):
    """Summarize text using Groq's llama model."""
    try:
        prompt = f"""Please summarize the following text from a web page.
Focus on the main points and key information.
Keep the summary concise but informative.

TEXT:
{text}

SUMMARY:"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1000
        )

        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"
def summarize_webpage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract visible text from paragraph tags
        paragraphs = soup.find_all("p")
        text = ' '.join([para.get_text() for para in paragraphs])

        # Limit to 3000 characters to avoid model input limits
        trimmed_text = text[:3000]

        # Run summarization
        summary = summarize_text(trimmed_text)
        return summary

    except Exception as e:
        return f"Error: {str(e)}"
      # Create Gradio interface
App = gr.Interface(
    fn=summarize_webpage,  # Function to summarize a webpage
    inputs=gr.Textbox(
        placeholder="Enter a webpage URL",
        label="Webpage URL"
    ),
    outputs=gr.Markdown(label="Summary"),
    title="Webpage Summarizer",
    description="""Enter any article or blog URL, and get a concise summary using Groq's large language models.""",
    examples=[
        ["https://www.geeksforgeeks.org/introduction-to-object-detection-using-image-processing/"],
        ["https://medium.com/@1511425435311/understanding-openais-temperature-and-top-p-parameters-in-language-models-d2066504684f"],

    ],
    allow_flagging="never"
)

App.launch()
