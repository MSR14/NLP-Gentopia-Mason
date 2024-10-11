from typing import AnyStr
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *
from pydantic import BaseModel, Field

class PDFReaderArgs(BaseModel):
    url: str = Field(..., description="A URL pointing to the PDF file.")

class PDFReader(BaseTool):
    """Tool that retrieves and reads a PDF file from a given URL."""

    name = "pdf_reader"
    description = ("A tool that downloads and reads the content of a PDF file from the provided URL."
                   "Input should be a URL pointing to a PDF file.")

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, url: AnyStr) -> str:
        try:
            # Download the PDF
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            
            # Read the PDF
            with BytesIO(response.content) as pdf_file:
                reader = PdfReader(pdf_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
            return text.strip()  # Return the extracted text
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    url = "https://arxiv.org/pdf/2001.04925.pdf"  # Example PDF URL
    pdf_content = PDFReader()._run(url)
    print(pdf_content)
