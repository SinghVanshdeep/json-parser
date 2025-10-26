
tokens = []
result = []

def json_constructor():
    json_string = ''
    for a_tok in tokens:
        if a_tok["type"] == "KEY_STRING":
            json_string += f' "{a_tok["value"]}" '
        elif a_tok["type"] == "VALUE_STRING":
            json_string += f' {a_tok["value"]}'
        else:
            json_string += f'{a_tok["value"]}'
    return json_string
    

def parser(file_size):
    result.clear()

    if not file_size:
        print("\nGiven File contains INVALID JSON. (Empty file)\nExit Code Status 1\n")
        return

    # handle empty JSON: {}
    elif len(tokens) == 2 and tokens[0]["type"] == "OPEN_BRACE" and tokens[1]["type"] == "CLOSE_BRACE":
        print("{}")
        print("\nGiven File contains VALID JSON. \nExit Code Status 0\n")
        return
    
    else:
        token_id = 0
        while token_id < len(tokens):
            curr = tokens[token_id]
            if curr["type"] == "OPEN_BRACE" and len(result) == 0:
                result.append(curr["type"])
            elif curr["type"] == "KEY_STRING" and (result[-1] == "OPEN_BRACE" or result[-1] == "COMMA"):
                result.append(curr["type"])
            elif curr["type"] == "COLON" and result[-1] == "KEY_STRING":
                result.append(curr["type"])
            elif curr["type"] == "VALUE_STRING" and result[-1] == "COLON":
                result.append(curr["type"])
            elif curr["type"] == "COMMA" and result[-1] == "VALUE_STRING":
                result.append(curr["type"])
            elif curr["type"] == "CLOSE_BRACE" and result[-1] == "VALUE_STRING":
                result.append(curr["type"])
            else:
                break
            token_id += 1
        if len(result) == len(tokens) and result[-1] == "CLOSE_BRACE":
            print(json_constructor())
            print("\nGiven File contains VALID JSON. \nExit Code Status 0\n")
        else:
            print(json_constructor())
            print("\nGiven File contains INVALID JSON. \nExit Code Status 1\n")


def helper(count, index, curr_string, main_text, open_brack, close_brack):
    curr_string += main_text[index]
    index += 1
    while index < len(main_text) and count > 0:
        if main_text[index] == open_brack:
            count += 1
        elif main_text[index] == close_brack:
            count -= 1
        curr_string += main_text[index]
        index += 1
    return curr_string
    

def lexer(file):
    tokens.clear()
    valid_size = True

    with open(file, "r") as f:
        text = f.read() # this reads the whole file as one big text

    if "'" in text:
        print("INVALID JSON, as a value is enclosed by '' \n")
        return

    elif len(text) < 1:
        valid_size = False
        parser(valid_size)
        return
    else:
        i = 0
        while i < len(text):
            if text[i] == '{' and len(tokens) == 0:
                tokens.append({"type": "OPEN_BRACE", "value": text[i]})
            elif text[i] == '"' and (tokens[-1]["type"] == "OPEN_BRACE" or tokens[-1]["type"] == "COMMA"):
                j = i+1
                key_string = ''
                while j < len(text) and text[j] != '"':
                    key_string += text[j]
                    j += 1
                i = j
                tokens.append({"type": "KEY_STRING", "value": key_string})
            elif text[i] == ":" and tokens[-1]["type"] == "KEY_STRING":
                tokens.append({"type": "COLON", "value": ":"})
                k = i+1
                while k < len(text) and text[k] == ' ': # skipping the space
                    k += 1

                value_string = ''
                # If it's a string
                if text[k] == '"':
                    k += 1 # move text[k] to the next char where it's not a "
                    while k < len(text) and text[k] != '"':
                        value_string += text[k]
                        k += 1
                
                elif text[k] == "'":
                    k += 1
                    while k < len(text) and text[k] != "'":
                        value_string += text[k]
                        k += 1
                    k += 1
                
                # Object value
                elif text[k] == '{':
                    bracket_count = 1
                    value_string += helper(bracket_count, k, value_string, text, '{', '}')
                
                # Array value
                elif text[k] == '[':
                    bracket_count = 1
                    value_string += helper(bracket_count, k, value_string, text, '[', ']')
                

                else: # anything other than a string
                    while k < len(text) and text[k] not in [',', '}']:
                        value_string += str(text[k])
                        k += 1
                value_string = value_string.strip()

                # JSON Single quote and literal check
                if value_string in ["True", "False", "NaN", "undefined", "None"] or "'" in value_string:
                    tokens.append({"type": "INVALID_VALUE", "value": value_string})
                else:
                    tokens.append({"type": "VALUE_STRING", "value": value_string})
                i = k - 1
            elif text[i] == ',' and tokens[-1]["type"] == "VALUE_STRING":
                tokens.append({"type": "COMMA", "value": ","})
            
            elif text[i] == '}' and (tokens[-1]["type"] == "VALUE_STRING" or tokens[-1]["type"] == "OPEN_BRACE"):
                tokens.append({"type": "CLOSE_BRACE", "value": "}"}) 
            i += 1
        # print(f'index - {i} and {len(tokens)}')
    parser(valid_size)

try:
    while True:
        file_name = input("Enter the JSON file you would like to parse: ")
        try:
            lexer(file_name)
        except FileNotFoundError:
            print("Enter a valid .json file\n")
except KeyboardInterrupt:
    print("\nProgram was closed due to Ctrl+C")
        
