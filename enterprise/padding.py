import base64

def add_padding(encoded_string):
    # Calculate the number of padding characters needed
    padding = 4 - (len(encoded_string) % 4)
    
    # Add the padding characters
    padded_string = encoded_string + "=" * padding
    
    return padded_string