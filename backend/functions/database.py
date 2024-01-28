import json
import random


# get recent messages
def get_recent_messages():
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

    data = None
    try:
        with open("functions/stored_data.json", "r") as read_file:
            data = json.load(read_file)
        if data:
            if len(data) < 5:
                for item in data:
                    messages.append(item)
            else:
                for item in data[-5:]:
                    messages.append(item)
    except json.JSONDecodeError as e:
        pass
    except Exception as e:
        return e
    return messages


def store_messages(request_message, response_message):
    messages = get_recent_messages()[1:]

    # add messages 
    user_message = {
        "role": "user",
        "content": request_message
    } 
    assistant_message = {
        "role": "assistant",
        "content": response_message
    } 
    messages.append(user_message)
    messages.append(assistant_message)
    # save file
    with open('functions/stored_data.json', 'w') as f:
        json.dump(messages, f)


def reset_messages():
    with open('functions/stored_data.json', 'w') as f:
        pass
        