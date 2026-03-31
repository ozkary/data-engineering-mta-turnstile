# gcs_server.py
from fastmcp import FastMCP
from google.cloud import storage
import fnmatch
import os

#Initialize FastMCP
mcp = FastMCP("GCS_Toolset")

# Initialize GCS Client (Uses GOOGLE_APPLICATION_CREDENTIALS)
# Ensure your environment variable points to your service account key
client = storage.Client()

@mcp.tool()
def list_mta_files(bucket_name: str, pattern: str = "*.gz") -> list[str]:
    """
    Action: Lists files in a GCS bucket that match a specific pattern.
    Useful for finding specific MTA data batches.
    """
    try:
        bucket = client.bucket(bucket_name)
        blobs = client.list_blobs(bucket)
        names = [b.name for b in blobs]
        # Filter using the glob pattern
        return fnmatch.filter(names, pattern)
    except Exception as e:
        return [f"Error: {str(e)}"]

@mcp.tool()
def read_file_preview(bucket_name: str, file_name: str, limit_bytes: int = 1000) -> str:
    """
    Action: Reads a small preview of a file's content to inspect headers or data format.
    """
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        # Download a small chunk to avoid memory issues with large .gz files
        content = blob.download_as_bytes(start=0, end=limit_bytes)
        return content.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.resource("mta://discovery/rules")
def get_discovery_rules() -> str:
    """
    Returns the technical specifications for MTA file discovery.
    This guide defines the folder structure and naming conventions.
    """
    return """
    # MTA Discovery Rules
    - Source System: The top-level folder name (e.g., 'turnstile') represents the Namespace.
    - Historical Data: YYYYYMMDD.csv.gz
    - Real-time Feed: YYYMMDDHHMM.json
    - File Pattern: Look for '.gz' extensions.
    - Date Pattern: Files must follow the ISO date format (YYYYMMDD) within the filename.
    - Validation: Any file not matching 'YYYYMMDD.csv.gz' should be flagged as 'Unknown'.
    """

@mcp.prompt()
def identify_mta_batches(bucket: str):
    return f"""
    - Read the resource 'mta://discovery/rules' to understand what we are looking for.
    - Use 'list_gcs_files' on bucket '{bucket}'.
    - Identify which files match the 'Historical Data' pattern.
    - Report back the batches ready for ingestion.
    """

if __name__ == "__main__":
    mcp.run()