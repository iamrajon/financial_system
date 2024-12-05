import logging
import time
from logging.handlers import RotatingFileHandler
from django.http import JsonResponse

# Create Logger instance
logger = logging.getLogger("api_logger")

# File Handler with log rotation
file_handler = RotatingFileHandler(
    "logs/api_requests.log", maxBytes=5 * 1024 * 1024, backupCount=5
)

# Console Handler
# console_handler = logging.StreamHandler()

# Formatter for logs
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s; %(message)s")
file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
# logger.addHandler(console_handler)

# Set logging level
logger.setLevel(logging.INFO)
# logger.setLevel(logging.ERROR)


class APILoggingMiddleware:
    """
    Middleware for logging incoming API requests and handling errors.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Logic executed before the request is passed to the view
        start_time = time.time()
        request_data = {
            "method": request.method,
            "ip_address": request.META.get("REMOTE_ADDR"),
            "path": request.path,
        }

        # Log the incoming request
        logger.info(f"Incoming request: {request_data}")

        # Process the request and handle any exceptions
        
        try:
            response = self.get_response(request)
        except Exception as e:
            # Log the error with traceback
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            error = str(e)
            # Return a standardized error response
            return JsonResponse(
                {"error": "An error occurred while processing your request."},
                status=500,
            )

        # Logic executed after the view is called
        duration = time.time() - start_time
        response_data = {
            "status_code": response.status_code,
            "duration": duration,
        }
        logger.info(f"Response data: {response_data}")

        return response
