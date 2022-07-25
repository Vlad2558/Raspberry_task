import csv


class CSV_File:
    """
    Class to Read and Write CSV File.
    """

    def __init__(self, file_path):
        """
        Choose file to work with it.
        :param file_path:
        """
        self.path = file_path

    def read_csv(self, index=None):
        """
        Try to read csv file.
        :param index:
        use index to get only one result.
        :return:
        Return all results or correct one by index.
        """
        try:
            with open(self.path, "r") as file:
                data = []
                for el in file.read().splitlines():
                    data.append(el.split(","))
                if index:
                    return data[index]
                else:
                    return data
        except FileNotFoundError:
            print("File not Found")
            return None

    def send_to_csv(self, send_data: dict):
        """
        Send new data CSV file.
        :param send_data:
        Data to send.
        """
        fieldnames = ["first_number", "second_number"]
        data = {"first_number": send_data["first_number"], "second_number": send_data["second_number"]}
        try:
            with open(self.path, "r"):
                pass
            with open(self.path, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow(data)

        except FileNotFoundError:
            with open(self.path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(data)

    def csv_limit(self, limit: int):
        """
        Set limit in count of rows on Csv file.
        :param limit:
        count of rows.
        """
        fieldnames = ["first_number", "second_number"]
        try:
            with open(self.path, "r") as read_file:
                reader = csv.DictReader(read_file)
                data = []
                for row in reader:
                    data.append({"first_number": row["first_number"], "second_number": row["second_number"]})
        except FileNotFoundError:
            print("File not Found")
            return None
        if len(data) > limit:
            data.pop(0)
            with open(self.path, "w", newline="") as write_file:
                writer = csv.DictWriter(write_file, fieldnames=fieldnames)
                writer.writeheader()
                for el in data:
                    writer.writerow(el)
