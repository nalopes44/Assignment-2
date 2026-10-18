from math import sqrt


class Predictor:

    def __init__(self, historical_data):
        """
        Store historical DataTable.
        """
        # Enforce abstract behavior without importing abc.
        if type(self).predict is Predictor.predict:
            raise TypeError("Predictor subclasses must implement predict().")
        self.historical_data = historical_data

    def predict(self, patient):
        """
        Make a prediction for one patient.
        """
        raise NotImplementedError("Subclasses must implement predict().")


class MajorityClassPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)
        tumor_types = historical_data.get_column("TumorType")
        if not tumor_types:
            raise ValueError("Historical data must contain at least one patient.")

        counts = {}
        for tumor_type in tumor_types:
            counts[tumor_type] = counts.get(tumor_type, 0) + 1

        # If counts tie, use the outcome encountered first in the data.
        self.majority_class = max(counts, key=counts.get)

    def predict(self, patient):
        """
        Always return the most common historical TumorType.
        """
        return self.majority_class


class NearestNeighborPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)
        if not historical_data.data:
            raise ValueError("Historical data must contain at least one patient.")

    def distance(self, patient1, patient2):
        """
        Calculate Euclidean distance using Feature1-Feature9 only.
        """
        squared_distance = 0.0
        for feature_number in range(1, 10):
            feature_name = f"Feature{feature_number}"
            difference = patient1[feature_name] - patient2[feature_name]
            squared_distance += difference ** 2
        return sqrt(squared_distance)

    def predict(self, patient):
        """
        Find closest historical patient and return its TumorType.
        """
        closest_patient = self.historical_data.data[0]
        smallest_distance = self.distance(patient, closest_patient)

        for row_idx in range(1, len(self.historical_data.data)):
            historical_patient = self.historical_data.data[row_idx]
            distance = self.distance(patient, historical_patient)
            if distance < smallest_distance:
                smallest_distance = distance
                closest_patient = historical_patient

        # Equal distances keep the first matching historical patient.
        return closest_patient["TumorType"]
