import openai
import logging
from openai.error import RateLimitError, InvalidRequestError, OpenAIError  # Import error classes from openai.error
from django.conf import settings

# Set OpenAI API key from settings.py
openai.api_key = settings.OPENAI_API_KEY

class InsufficientQuotaError(Exception):
    """Raised when the OpenAI API quota is exceeded."""
    pass

class RateLimitExceededError(Exception):
    """Raised when the OpenAI API rate limit is exceeded."""
    pass

def get_answer(question, document_text):
    try:
        # Construct the prompt for OpenAI API
        prompt = f"Given the following document, answer the question.\n\nDocument: {document_text}\n\nQuestion: {question}\nAnswer:"

        # Make the API request to OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the appropriate model engine
            prompt=prompt,
            max_tokens=150,  # Adjust tokens as needed
            temperature=0.7,  # Controls randomness/creativity
            top_p=1.0,  # Sampling strategy
            n=1,  # Only return one response
            stop=["\n"]  # Stop at the end of the answer
        )

        # Extract the answer from the response
        answer = response['choices'][0]['text'].strip()
        return answer

    except RateLimitError:  # Handle rate limit errors directly
        logging.error("OpenAI API rate limit exceeded.")
        raise RateLimitExceededError("OpenAI API rate limit exceeded.")
    
    except InvalidRequestError:  # Handle insufficient quota or invalid requests
        logging.error("Insufficient quota in your OpenAI account.")
        raise InsufficientQuotaError("Insufficient quota available in your OpenAI account.")
    
    except OpenAIError as e:  # Handle other OpenAI-related errors
        logging.error(f"OpenAI API error: {str(e)}")
        return f"OpenAI API error: {str(e)}"
    
    except Exception as e:  # Handle unexpected errors
        logging.error(f"An unexpected error occurred: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"
