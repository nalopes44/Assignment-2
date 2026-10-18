class DataTable:
    def __init__(self, csv_path: str):
        """
        Load CSV data into memory.
        Convert all values to float.
        """
        with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
            header = csv_file.readline().strip()
            self._column_names = header.split(",") if header else []
            self._column_names = [name.strip() for name in self._column_names]
            self.data = []
            for line in csv_file:
                if not line.strip():
                    continue
                values = [value.strip() for value in line.strip().split(",")]
                if len(values) != len(self._column_names):
                    raise ValueError("Each CSV row must match the column names.")
                self.data.append(dict(zip(self._column_names, values)))

        missing_columns = []
        for name in self._column_names:
            if any(row[name].strip() == "?" for row in self.data):
                missing_columns.append(name)

        # New cases use the matching historical file in the same directory.
        historical_rows = self.data
        directory, separator, filename = str(csv_path).rpartition("/")
        if missing_columns and filename.startswith("cancer_new_cases"):
            historical_path = directory + separator + filename.replace(
                "cancer_new_cases", "cancer_historical", 1
            )
            with open(historical_path, newline="", encoding="utf-8-sig") as csv_file:
                historical_columns = [
                    name.strip() for name in csv_file.readline().strip().split(",")
                ]
                historical_rows = []
                for line in csv_file:
                    if not line.strip():
                        continue
                    values = [value.strip() for value in line.strip().split(",")]
                    if len(values) != len(historical_columns):
                        raise ValueError("Each CSV row must match the column names.")
                    historical_rows.append(dict(zip(historical_columns, values)))

        # Calculate means before replacing any missing values.
        means = {}
        for name in missing_columns:
            valid_values = []
            for row in historical_rows:
                if row[name].strip() != "?":
                    valid_values.append(float(row[name]))
            if not valid_values:
                raise ValueError(
                    f"Cannot fill missing values in {name!r}: "
                    "the historical column has no valid numeric values."
                )
            means[name] = sum(valid_values) / len(valid_values)

        for row in self.data:
            for name in self._column_names:
                if row[name].strip() == "?":
                    row[name] = means[name]
                else:
                    row[name] = float(row[name])

    def get(self, row_idx: int, col_name: str):
        """
        Return a single value from a row and column.
        """
        return self.data[row_idx][col_name]

    def get_column(self, col_name: str) -> list:
        """
        Return all values in a column.
        """
        if col_name not in self._column_names:
            raise KeyError(col_name)
        return [row[col_name] for row in self.data]

    def get_row(self, row_idx: int) -> dict:
        """
        Return a row as {column_name: value}
        """
        return self.data[row_idx].copy()

    def get_column_names(self) -> list:
        """
        Return list of column names.
        """
        return self._column_names.copy()

    def get_column_average(self, col_name: str) -> float:
        """
        Return average of a column.
        """
        values = self.get_column(col_name)
        if not values:
            raise ValueError(f"Cannot average empty column {col_name!r}.")
        return sum(values) / len(values)

    def get_column_min(self, col_name: str) -> float:
        """
        Return minimum value of a column.
        """
        return min(self.get_column(col_name))

    def get_column_max(self, col_name: str) -> float:
        """
        Return maximum value of a column.
        """
        return max(self.get_column(col_name))
