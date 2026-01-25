from datetime import datetime

log_folder = "test_logs"

dump_log_file = f"{log_folder}/.log"
complete_log_file = f"{log_folder}/000_general.log"

log_levels = {
    "default": {
        "filename": "001_dafault",
        "variable": "[LOG]    ",
        "hash_code": "11111111111111111111111111111111"
    },
    "debug": {
        "filename": "002_debug",
        "variable": "[DEBUG]  ",
        "hash_code": "22222222222222222222222222222222"
    },
    "error": {
        "filename": "003_error",
        "variable": "[ERROR]  ",
        "hash_code": "33333333333333333333333333333333"
    },
    "warning": {
        "filename": "004_warning",
        "variable": "[WARNING]",
        "hash_code": "44444444444444444444444444444444"
    }
}

def normalize(strng):
    if len(strng) > 32:
        return strng[:32]
    else:
        for _ in range(32 - len(strng)):
            strng += "."
        return strng

def new_log(message, hash, log_level):
    time = datetime.now()

    log_line = f"[{time}] {log_levels[log_level]["variable"]} > {message.replace("\n", f"\n  \\------------------------] {log_levels[log_level]["variable"]} > ")}"

    for level in log_levels:
        if hash == log_levels[level]["filename"] and level != log_level:
            hash = log_levels[log_level]["filename"]
            break

    with open(f"{log_folder}/{hash}.log", "a") as log_file: log_file.write(log_line + "\n")

    code_32 = hash

    if hash == log_levels[log_level]["filename"]:
        with open(f"{complete_log_file}", "a") as log_file: log_file.write(log_line + "\n")
        print(log_line)
        # code_32 = log_levels[log_level]["hash_code"] # better to keep filename reference for better log management


    informative_log_line = f"[{time}] ({normalize(code_32)}) {log_levels[log_level]["variable"]} > {message.replace("\n", f"\n  \\------------------------] ({normalize(code_32)}) {log_levels[log_level]["variable"]} > ")}"

    with open(f"{dump_log_file}", "a") as log_file: log_file.write(informative_log_line + "\n")

def log(message, hash=log_levels["default"]["filename"]):
    new_log(message, hash, "default")

def debug(message, hash=log_levels["debug"]["filename"]):
    new_log(message, hash, "debug")

def error(message, hash=log_levels["error"]["filename"]):
    new_log(message, hash, "error")

def warning(message, hash=log_levels["warning"]["filename"]):
    new_log(message, hash, "warning")