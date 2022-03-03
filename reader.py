
def read(file_path):
    """
    :param file_path: The filepath of the RINEX file
    :return: general data as list of dictionary format
    [{
        "year": ,
        "month": ,
        "day": ,
        "lol": true/false
    },
    ... ]
    """
    return []


def get_header(file_path):
    header_text = []
    with open(file_path, "r") as f:
        is_header = True
        for line in f.readlines():
            is_header = line.strip() != "END OF HEADER"
            if is_header:
                header_text.append(line[:60])
            else:
                return header_text
            current_line = f.readline()
            #header_text.append([x.strip() for x in current_line.split(" ")])


def fetch_next_block(expected_line):
    """
    Returns the codeblock, given an expected line and updates the expected line for the next block
    :param expected_line: line where the block is expected. Self-correcting if conservative
    :return: next expected line, data
    """
    # TODO Read Block header
    # TODO Update expected line
    return [expected_line]


if __name__ == "__main__":
    print("\n".join(get_header("repro.goce2640.13o")))
