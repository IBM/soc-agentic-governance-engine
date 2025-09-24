from typing import Union
from io import BytesIO
from typing import Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import base64
import PyPDF2  # Make sure to install PyPDF2: pip install PyPDF2
import os
import tempfile
import subprocess
import pandas as pd


# creating a tool to process a PDF file input of which is in bytes format
@tool(name="file_upload", description="Allow the user upload the file from chat and take that in as bytes to process it", permission=ToolPermission.ADMIN)
def process_uploaded_file(file_bytes: bytes) -> str:
    """
    Processes the uploaded XLSX file and returns the context as a string.

    :param file_bytes: The bytes of the uploaded XLSX file.
    :returns text: A string containing the link to the processed file.
    """
    
    # Convert bytes to BytesIO object
    file_stream = BytesIO(file_bytes)
    
    df = pd.read_excel(file_stream)
    return df['Checklist'].tolist()
