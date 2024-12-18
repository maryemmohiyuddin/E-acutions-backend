from bids.tasks import auction_end_task
from datetime import datetime
import pytz
from celery import Celery

def schedule_auction_task(auction_id, end_time):
    karachi_tz = pytz.timezone('Asia/Karachi')

    # Check if end_time is naive (i.e., without timezone)
    if end_time.tzinfo is None:
        # Localize if naive
        end_time_utc = karachi_tz.localize(end_time).astimezone(pytz.utc)
    else:
        # If it's already timezone-aware, just convert to UTC
        end_time_utc = end_time.astimezone(pytz.utc)

    # Schedule the task using Celery with a specific execution time (eta=end_time_utc)
    auction_end_task.apply_async(args=[auction_id, end_time], eta=end_time_utc)

    # Optionally, log the scheduled task time (useful for debugging)
    print(f"Task scheduled for auction {auction_id} at {end_time_utc}")
