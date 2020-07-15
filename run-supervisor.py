from pathlib import Path
import sys
import subprocess


def extract_data(path):
    parts = path.parts
    modality = parts[len(parts) - 2]
    collection = parts[len(parts) - 3]
    number = parts[len(parts) - 1].split(".")[0]
    return " ".join([str(path), modality, collection, number])


data_root_path = sys.argv[1]
output_path = sys.argv[2]
exe_path = sys.argv[3]
config_path = sys.argv[4]
result_path = sys.argv[5]
logs_file = sys.argv[6]

paths = [path.absolute() for path in list(Path(data_root_path).rglob("*.cimg"))]
paths_with_data = [extract_data(path) for path in paths]

with open(output_path, mode="wt", encoding="utf-8") as output:
    output.write("\n".join(paths_with_data))

lines = 0
with open(result_path) as file:
    lines = len(file.readlines()) - 1
    if lines == -1:
        lines = 0

with open(logs_file, "a+") as logs:
    exit_code = subprocess.call([exe_path, output_path, config_path, result_path, str(lines)], stdout=logs, stderr=logs)
    print(f"Subprocess exited with {exit_code}")
