import numpy as np


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
    :return: connection matrix

    Matrix codes:
     0: disconnected    -> doesn't show up
     1: connected, lock
     2: no lock         -> 0 in the file

    """
    expected_line_start = " " + str(year)[-2:] + " "
    with open(filepath, "r") as f:
        header = get_header(f)                                      # If needed
        file_line = "."
        num_observation = 8  # Set to constant for now. actual number in header
        lines_per_satellite = num_observation // 5 + 1
        line_count = len(header)                                    # For troubleshooting
        epoch_count = 0                                                 # The returning array
        connection_matrix = np.zeros([86400, 32], np.byte)
        while file_line:
            ##if line_count > 100:
              ##  return {}  # For debugging
            file_line = f.readline()
            line_count += 1
            """
            [
                [0, 0, data, 0, 0],
                [0, 0, data, 0, 0],
                ...
            ]
            """
            if file_line.startswith(expected_line_start):
                data = file_line.split()[:-1]                       # Separates line
                date = [int(x) for x in data[:5]]                   # First 5 integers of the date
                date.append(float(data[5]))                         # Seconds indicator
                epoch_flag = int(data[6])                           # Fetches phase bit
                #print(f"Date: {date}")
                if epoch_flag != 0:
                    print(epoch_flag)
                if epoch_flag < 2:                                  # Case: 'OK'
                    sattelite_count = int(data[7])                  # Next is the number of availble satellites
                    satellite_indecies = [int(x) for x in data[8: 8+sattelite_count]]

                    for s in satellite_indecies:
                        connection_matrix[epoch_count][s-1] = 1

                    lol = []
                    for i in range(sattelite_count):
                        text = "".join(f.readline() for i in range(lines_per_satellite))
                        text.replace("\n", "")  # Get rid of the newlines
                        data = [float(x) for x in text.split()]
                        if 0 in data[:-1]:
                            connection_matrix[epoch_count][satellite_indecies[i] - 1] = 2
                        else:
                            connection_matrix[epoch_count][satellite_indecies[i] - 1] = 1
                            #lol_satellite = satellite_indecies[i]
                            ##print(lol_satellite)
                            #lol.append(lol_satellite)
                    #print(lol)

                elif 2 <= epoch_flag < 6:                       # TODO: What to do exactly if the epoch flag is not 'OK'
                    sattelite_count = int(data[7])
            epoch_count += 1

    return connection_matrix


def compartementalizer(matrix):
    """
    takes matrix ->
    :return: sattelite track
    """
    all_tracks = []
    for satellite in matrix.transpose():
        current_track = []
        connected = False
        for x in satellite:
            if x == 0 and connected:
                # stopped track
                all_tracks.append(current_track)
                connected = False
            elif x != 0 and not connected:
                # start track
                current_track = []
                connected = True
            if x != 0:
                current_track.append(x)
    return all_tracks


def check_for_lol(satellite_tracks):
    count = 0
    for satellite in satellite_tracks:  # outer list
        while satellite != [] and satellite[0] == 2:
            satellite.pop(0)
        while satellite != [] and satellite[-1] == 2:
            satellite.pop()
        if 2 in satellite:
            print(satellite.count(2))
        for data in satellite[1:-1]:
            if data == 2:
                count += 1
    print(count)


if __name__ == "__main__":
    res = read("red.goce2460.13o/repro.goce2460.13o", 2013)
    satellite_tracks = compartementalizer(res)
    print(len(satellite_tracks))
    check_for_lol(satellite_tracks)

"""
file -> connection matrix 86400 x 32 0,1,2
connection matrix -> 502 tracking arrays
"""

# 2:39:57
