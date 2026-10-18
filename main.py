from data_representation import DataTable
from predictors import MajorityClassPredictor, NearestNeighborPredictor
from exceptions import OutOfSampleError


def calculate_accuracy(predictions, actual):
    """
    Return the fraction of predictions that match the actual outcomes.
    """
    if len(predictions) != len(actual):
        raise ValueError("Predictions and actual outcomes must have the same length.")
    if not actual:
        raise ValueError("Cannot calculate accuracy without any outcomes.")

    correct = 0
    for prediction, outcome in zip(predictions, actual):
        if prediction == outcome:
            correct += 1
    return correct / len(actual)


def main():

    # Load datasets
    historical = DataTable("Data/cancer_historical1.csv")
    new_cases = DataTable("Data/cancer_new_cases1.csv")
    labels = DataTable("Data/cancer_new_cases_labels1.csv")
    actual_labels = labels.get_column("TumorType")
    if len(new_cases.data) != len(actual_labels):
        raise ValueError("Each new case must have exactly one true outcome.")


    # Create predictors
    mode_predictor = MajorityClassPredictor(historical)
    nn_predictor = NearestNeighborPredictor(historical)


    mode_predictions = []
    nn_predictions = []
    evaluated_labels = []
    skipped_cases = 0


    # Predict every new case
    for i in range(len(new_cases.data)):

        patient = new_cases.get_row(i)

        try:
            mode_prediction = mode_predictor.predict(patient)
            nn_prediction = nn_predictor.predict(patient)

        except OutOfSampleError as e:
            print(f"{type(e).__name__}: {e}")
            skipped_cases += 1
            continue

        mode_predictions.append(mode_prediction)
        nn_predictions.append(nn_prediction)
        evaluated_labels.append(actual_labels[i])

    if skipped_cases:
        print(f"Skipped {skipped_cases} out-of-sample cases; accuracy uses the remaining cases.")
    if not evaluated_labels:
        print("No valid cases available to calculate accuracy.")
        return


    # Accuracy
    print(
        f"Mode accuracy: {calculate_accuracy(mode_predictions, evaluated_labels):.2%}"
    )

    print(
        f"Nearest Neighbor accuracy: {calculate_accuracy(nn_predictions, evaluated_labels):.2%}"
    )


if __name__ == "__main__":
    main()
