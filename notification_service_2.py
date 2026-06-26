import time

# RULEBOOK
# How many notifications allowed, and in how many seconds
limits = {
    "Status Update": {"max": 2, "seconds": 60},
    "Marketing":     {"max": 3, "seconds": 3600},
    "News":          {"max": 1, "seconds": 86400},
}

# DIARY
# Stores when we sent notifications to each user
diary = {}

def send_notification(user, ntype, message):

    # Step 1: Is this a valid type?
    if ntype not in limits:
        print("BLOCKED - Unknown type")
        return

    max_allowed = limits[ntype]["max"]
    time_window = limits[ntype]["seconds"]

    # Step 2: Create diary entry for this user if not exists
    if user not in diary:
        diary[user] = {}

    if ntype not in diary[user]:
        diary[user][ntype] = []

    # Step 3: Remove old timestamps from diary
    now = time.time()
    cutoff = now - time_window

    fresh_times = []
    for t in diary[user][ntype]:
        if t > cutoff:
            fresh_times.append(t)

    diary[user][ntype] = fresh_times

    # Step 4: Count how many times sent recently
    count = len(diary[user][ntype])

    # Step 5: Allow or block
    if count < max_allowed:
        diary[user][ntype].append(now)
        print("SENT -", message)
    else:
        print("BLOCKED - Too many notifications")


# ---------- TESTING ----------

send_notification("alice", "Status Update", "Server is up")    # SENT
send_notification("alice", "Status Update", "Server is down")  # SENT
send_notification("alice", "Status Update", "Server is up")    # BLOCKED

send_notification("alice", "News", "Big news today")           # SENT
send_notification("alice", "News", "Another news")             # BLOCKED

send_notification("alice", "Marketing", "Sale starts now")     # SENT
send_notification("alice", "Marketing", "Free shipping")        # SENT
send_notification("alice", "Marketing", "Limited time offer")   # SENT
send_notification("alice", "Marketing", "New product launch")   # BLOCKED
