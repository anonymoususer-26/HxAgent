def serialize(array, default_keyword = "STEP"):
    plan = ""
    for i, content in enumerate(array):
        plan += default_keyword + " #" + str(i+1)+': '+str(content)+'\n'
    return plan

def remove_whitespace(content: str) -> str:
    content = content.replace(" ", "")
    content = content.replace("\t", "").replace("\n", "").replace("\r", "")
    content = content.replace('"', '').replace("'", '')
    return content