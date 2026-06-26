Rate-Limited Notification Service - Walkthrough Document

Overview

This project is a back-end utility that handles sending notifications 
(Email and SMS) to users. To prevent spamming, the system enforces 
strict rate limits based on the notification type using a sliding time 
window approach. All data is stored in-memory using Python dictionaries.


Project structure:

notification_service_2.py       → Main service file with inline manual test calls


How it works :

1. A request comes in via `send_notification(user, ntype, message)`.

2. The system checks if the notification type exists in the `limits` dictionary.
   If unknown → prints `BLOCKED - Unknown type` and returns.

3. It fetches the rate limit rules (`max` and `seconds`) from the `limits` dictionary.

4. It looks up the timestamp history for that user and notification type in `diary`.

5. It removes (prunes) all timestamps older than the current time window.
   This is the sliding window logic and also helps prevent history from growing without bound.

6. If the remaining timestamp count is less than the allowed limit →
   notification is sent, timestamp is saved, and the script prints `SENT - <message>`.

7. If the limit is already reached → the script prints `BLOCKED - Too many notifications`.

Manual test calls in `notification_service_2.py`:

**Test Cases:**

| Test ID | Description | Expected | Result |
|---|---|---|---|
| TC-01 | Single send under limit | True | PASSED |
| TC-02 | 3rd send in same minute | False | PASSED |
| TC-03 | Send after window resets | True | PASSED |
| TC-04 | Different user not affected | True | PASSED |
| TC-05 | Different type not affected | True | PASSED |

---




Key Design Decisions:

1. Config Dictionary
   All rate limit rules are stored in the `limits` dictionary. Adding a new notification type only requires adding a new entry to that dictionary.

2. Sliding Window
   The service prunes stale timestamps on every request, so usage is evaluated within the exact rolling time window.

3. Memory Leak Prevention
   Old timestamps are removed during each request so history does not grow indefinitely.

4. Simple Manual Testing
   The current implementation uses inline print-based tests in `notification_service_2.py` rather than a separate test suite.

Rate limit rules:


**Rate Limit Rules:**

| Notification Type | Max Limit | Time Window |
|---|---|---|
| Status Update | 2 | 60 seconds (1 minute) |
| Marketing | 3 | 3600 seconds (1 hour) |
| News | 1 | 86400 seconds (1 day) |

How to Run:

Step 1 - Run the script directly:

python notification_service_2.py

The script will print the result of each manual notification call.

