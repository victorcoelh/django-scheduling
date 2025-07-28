# Cache key template for storing per-user schedule data.
# The user's username is interpolated into the placeholder.
CACHE_KEY = "user_{}_schedule"

# Possible values for the 'status' field of the Task model.
# Used in the model's choices argument and for input validation.
POSSIBLE_TASK_STATUS = [
    ("PENDING", "Task pending"),
    ("ONGOING", "Task in progress"),
    ("DONE", "Task done"),
]
