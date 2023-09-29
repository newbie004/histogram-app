def read_intervals_and_samples(file_path):
    intervals = []
    samples = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                # Check if the line contains an interval in the format [start, end)
                if line.startswith("[") and line.endswith(")"):
                    try:
                        interval_parts = line[1:-1].split(",")
                        if len(interval_parts) == 2:
                            start = float(interval_parts[0])
                            end = float(interval_parts[1])
                            intervals.append((start, end))
                        else:
                            raise ValueError("Invalid interval format")
                    except ValueError:
                        # Handle invalid interval format
                        pass
                else:
                    try:
                        value = float(line)
                        samples.append(value)
                    except ValueError:
                        # Handle invalid values or non-float lines
                        pass

    return intervals, samples
