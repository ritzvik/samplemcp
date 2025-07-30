"""
Create a new experiment in Cloudera ML
"""

import os
import json
import subprocess
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional


def create_experiment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new experiment in Cloudera ML

    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: Project ID where the experiment will be created (required)
            - name: Name of the experiment (required)
            - description: Description of the experiment (optional)

    Returns:
        Dict with success flag, message, and experiment data
    """
    # Validate required parameters
    required_params = ["project_id", "name"]
    for param in required_params:
        if param not in params or not params[param]:
            return {"success": False, "message": f"Missing required parameter: {param}"}

    # Format host URL correctly
    host = config.get("host", "")
    if not host:
        return {"success": False, "message": "Missing host in configuration"}

    # Make sure host has the correct scheme
    parsed_url = urlparse(host)
    if not parsed_url.scheme:
        host = "https://" + host
    elif parsed_url.scheme and "://" in host[len(parsed_url.scheme) + 3 :]:
        # Fix potential double https:// in the URL
        host = parsed_url.scheme + "://" + host.split("://")[-1]

    api_key = config.get("api_key")
    if not api_key:
        return {"success": False, "message": "Missing api_key in configuration"}

    # Build the request data
    request_data = {"name": params["name"]}

    # Add description if provided
    if "description" in params and params["description"]:
        request_data["description"] = params["description"]

    # Format request data as JSON
    request_data_json = json.dumps(request_data)

    # Debug print URLs
    api_url = f"{host}/api/v2/projects/{params['project_id']}/experiments"
    print(f"Creating experiment with URL: {api_url}")

    # Construct curl command
    curl_cmd = [
        "curl",
        "-s",
        "-X",
        "POST",
        "-H",
        f"Authorization: Bearer {api_key}",
        "-H",
        "Content-Type: application/json",
        "-d",
        request_data_json,
        api_url,
    ]

    try:
        # Execute curl command
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # Check if the curl command was successful
        if result.returncode != 0:
            return {"success": False, "message": f"Failed to create experiment: {result.stderr}"}

        # Parse the response
        try:
            response = json.loads(result.stdout)

            # Check if there's an error in the response
            if "error" in response:
                return {
                    "success": False,
                    "message": f"API error: {response.get('error', {}).get('message', 'Unknown error')}",
                    "details": response.get("error", {}),
                }

            return {"success": True, "message": f"Successfully created experiment", "data": response}
        except json.JSONDecodeError:
            return {"success": False, "message": f"Failed to parse response: {result.stdout}"}

    except Exception as e:
        return {"success": False, "message": f"Error creating experiment: {str(e)}"}
