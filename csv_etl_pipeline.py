import csv # Import csv to read and write csv files

def extract_data(input_file): # Create extract function
    transformed_data = [] # Create an empty list to write the transformed data to
    try:
        with open(input_file, mode='r') as reader:
            csv_reader = csv.DictReader(reader)  # Use DictReader to read in rows as dictionaries

            columns = csv_reader.fieldnames

            columns_to_keep = [col for col in columns if "Score" in col or col == "Name"]  # Create list of fieldnames we want to keep based on criteria given

            for row in csv_reader:  # Loop through each row

                filtered_data = {col: row[col] for col in columns_to_keep}  # Creating new row dictionaries with only the columns we want
                transformed_data.append((filtered_data, columns_to_keep))

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found") # Error for when the file does not exist
    except PermissionError:
        print(f"Error: Do not have permission to read file '{input_file}'") # Error in the case of not having read permissions
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}") # General exception case

    return transformed_data, columns_to_keep

def transform(extracted_data):
    transformed_data = []

    for row, columns_to_keep in extracted_data:

        try:
            score_columns = [row[col] for col in columns_to_keep if "Score" in col]  # Specifically pick out score columns for average calculation

            if score_columns:
                average_score = sum(int(col) for col in score_columns) / len(score_columns)  # Computes the average score over all score columns

            row['Average Score'] = average_score  # Add the average score column
            transformed_data.append(row)

        except ValueError:
            print(f"Error: Invalid data in score columns")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")


    return transformed_data

def load(output_file, transformed_data, columns_to_keep):
    try:
        with open(output_file, mode="w", newline='') as writer:
            csv_writer = csv.DictWriter(writer, fieldnames=columns_to_keep + ['Average Score'])  # Use DictWriter as each row is a dictionary

            csv_writer.writeheader()
            csv_writer.writerows(transformed_data)
        return True

    except PermissionError:
        print(f"Error: You don't have permission to write to this file '{output_file}'") # If trying to overwrite existing file, this will happen if it is open
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return False

def main():
    input_file = "student_test_scores_extended(in).csv"
    output_file = "transformed_data.csv"

    try:
        extracted_data, columns_to_keep = extract_data(input_file)

        transformed_data = transform(extracted_data)

        if load(output_file, transformed_data, columns_to_keep): # This step checks if the load process succeeds

            print("Data extracted, transformed, and loaded to \"transformed_data.csv\"")

        else: print("Failure in loading process") # Prints alternative message if the process fails


    except Exception as e:
        print(f"Error: An unexpected error has occurred: {e}")


if __name__=="__main__":
    main()