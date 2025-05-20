import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_json_from_response(response_content):
    """
    Extracts a JSON object from a string response.

    Parameters:
    response_content (str): The response string from which to extract the JSON object.

    Returns:
    dict: The extracted JSON object as a Python dictionary, or None if parsing fails.
    """
    logger.debug("Raw response content: %s", response_content)
    try:
        # Directly parse the JSON string into a Python dictionary
        parsed_json = json.loads(response_content)
        logger.debug("Parsed JSON object: %s", parsed_json)
        return parsed_json
    except json.JSONDecodeError as e:
        logger.error("Error decoding JSON: %s", e)
        logger.error("Problematic JSON string: %s", response_content)
        # Attempt to trim the string to extract JSON
        start_index = response_content.find('{')
        end_index = response_content.rfind('}') + 1
        if start_index != -1 and end_index != -1:
            trimmed_content = response_content[start_index:end_index]
            try:
                parsed_json = json.loads(trimmed_content)
                logger.debug("Parsed JSON object after trimming: %s", parsed_json)
                return parsed_json
            except json.JSONDecodeError as e:
                logger.error("Error decoding JSON after trimming: %s", e)
                return None
        return None 