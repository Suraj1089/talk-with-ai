import json
import random


# get recent messages
def get_recent_messages():
    file_name = "stored_data.json"
    learn_instructions = {
        "role": "system",
        "content": "You are interviewing the user for a job as a ratail assistant. Ask questions that are relevant to the junior position. You name is Rachel. keep the answers under 30 sec."
    }

    # intialise messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instructions["content"] = learn_instructions["content"] + \
            "Your response will include some dry humour."
    else:
        learn_instructions["content"] = learn_instructions["content"] + \
            "Your response will include rather challenging questions."

    messages.append(learn_instructions)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)
        return

    return messages
