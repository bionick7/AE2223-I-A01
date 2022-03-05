
def get_header(f):
    """
    Returns the header text as list of strings
    :param f: The header file
    :return: All header lines, as list
    """
    header_text = []

    file_line = "."
    while file_line:
        file_line = f.readline()
        header_text.append(file_line[:-1])
        if file_line.strip() == "END OF HEADER":
            return header_text

    return header_text


def read(filepath, year):
    """
    :param filepath: The filepath of the RINEX file
    :param year: The year the observation was taken on
    :return: general data as list of dictionary format
    [{
        "date": [year, month, day, hour, minute, second],
        "satellite count": ...,
        "lol": true/false,
        "lol indicators": [ ... satellite count ... | 0 <= x <= 7],
        "signal strengths": [ ... satellite count ... | 0 <= x <= 9],
        (optional)"event": ...
    },
    ... ]
    """
    expected_line_start = " " + str(year)[-2:]
    with open(filepath, "r") as f:
        header = get_header(f)                                      # If needed
        file_line = "."
        line_count = len(header)                                    # For troubleshooting
        res = []                                                    # The returning array
        while file_line:
            file_line = f.readline()
            line_count += 1
            if file_line.startswith(expected_line_start):
                data = file_line.split()[:-1]                       # Separates line
                date = [int(x) for x in data[:5]]                   # First 5 integers of the date
                date.append(float(data[5]))                         # Seconds indicator
                epoch_flag = int(data[6])                           # Fetches phase bit
                if epoch_flag < 2:                                  # Case: 'OK'
                    sattelite_count = int(data[7])                  # Next is the number of availble sattelites
                    lli = []                                        # Loss of Lock indicators 0-7
                    strength = []                                   # Strength indicators     0-9
                    for t in data[8: 8+sattelite_count]:
                        if len(t) == 1:
                            lli.append(0)                           # Get if bit set by '(bit & lli != 0)'
                            strength.append(int(t))
                        elif len(t) == 2:
                            lli.append(int(t[0]))
                            strength.append(int(t[1]))
                        else:                                       # Sanity check
                            print(f"ERROR: invalid date ({data}) at line {line_count} in file {filepath}")
                    lol = False                                 # TODO: What indicated lol in the end ?
                    res.append({
                        "date": date,
                        "satellite count": sattelite_count,
                        "lol": lol,
                        "lol indicators": lli,
                        "signal strengths": strength
                    })
                elif 2 <= epoch_flag < 6:                       # TODO: What to do exactly if the epoch flag is not 'OK'
                    sattelite_count = int(data[7])
                    res.append({
                        "date": date,
                        "satellite count": sattelite_count,
                        "event": epoch_flag
                    })
    return res


if __name__ == "__main__":
    res = read("repro.goce2640.13o", 2013)
    print(res[0])
