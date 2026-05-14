import csv
import os

FILE_NAME = "dataset.csv"

def save_to_dataset(bsm, decision):

    # Check if file already exists
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode='a', newline='') as file:

        writer = csv.writer(file)

        # Write column headers only once
        if not file_exists:

            writer.writerow([
                "vehicle_id",
                "timestamp",
                "latitude",
                "longitude",
                "speed",
                "event",
                "decision"
            ])

        # Write BSM data row
        writer.writerow([
            bsm["vehicle_id"],
            bsm["timestamp"],
            bsm["latitude"],
            bsm["longitude"],
            bsm["speed"],
            bsm["event"],
            decision
        ])