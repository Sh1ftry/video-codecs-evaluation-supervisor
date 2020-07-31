from pathlib import Path
import sys
import subprocess

logs_path = Path("./process.log")
results_root_path = Path("./results")

data_root_paths = [Path("./data"), Path("./data-packed")]

for data_root_path in data_root_paths:
    paths = [str(path.absolute()) for path in list(data_root_path.rglob("*.cimg"))]
    paths_path = data_root_path.with_suffix(".paths")
    with open(paths_path, mode="wt", encoding="utf-8") as output:
        output.write("\n".join(paths))


class Encoder:
    def __init__(self, name, config_path):
        self.exe_path = Path(f"./{name}.sh").absolute()
        self.results_path = results_root_path / name
        self.config_path = config_path


encoders = [
    Encoder("jp3d", None),
    Encoder("HEVCEncoder", Path("hevc.cfg")),
    Encoder("VVCEncoder", Path("vvc.cfg")),
]


def count_lines(path):
    lines = 0
    try:
        with open(path) as file:
            lines = len(file.readlines()) - 1
            if lines == -1:
                lines = 0
    except FileNotFoundError:
        lines = 0
    return lines


with open(logs_path, "a+") as logs:
    for encoder in encoders:
        for data_root_path in data_root_paths:
            process_args = [
                encoder.exe_path.absolute(),
                data_root_path.with_suffix(".paths").absolute(),
            ]
            if encoder.config_path is not None:
                process_args.append(encoder.config_path.absolute())
            encoder.results_path.mkdir(parents=True, exist_ok=True)
            results_path = (encoder.results_path / data_root_path.name).with_suffix(".csv")
            processed_lines = count_lines(results_path)
            process_args.append(results_path.absolute())
            process_args.append(processed_lines)
            process_args_stringified = [str(arg) for arg in process_args]
            print(f"Launching subprocess {process_args_stringified}")
            exit_code = subprocess.call(process_args_stringified, stdout=logs, stderr=logs)
            print(f"{encoder.exe_path} subprocess exited with {exit_code}")
