from datetime import datetime
from pathlib import Path

import click
from pandas import DataFrame, read_csv

FILE_PATH = Path(__file__).resolve()
PROJECT_FOLDER = FILE_PATH.parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"
SOURCE_FILE = DATA_FOLDER / "source" / "meaning.csv"
RESULT_FOLDER = DATA_FOLDER / "result"


def get_sample_dataframe(required_observation, raw_file=SOURCE_FILE):
    dataframe = read_csv(raw_file)
    sample_dataframe = dataframe.sample(n=required_observation)
    return sample_dataframe


def get_current_time():
    current_time = datetime.now()
    current_time_text = current_time.strftime("%Y_%m_%d_%H_%M")
    return current_time_text


def main(destination_folder=RESULT_FOLDER):
    question_bank = get_sample_dataframe(required_observation=3, raw_file=SOURCE_FILE)

    response_list = []
    # loop over each obsevation and ask question
    for _, row in question_bank.iterrows():
        response = click.prompt(text=row["word"], type=str)

        # save the response to dataframe for same keyword
        response_list.append(
            {"word": row["word"], "response": response, "answer": row["meaning"], "correct": ""}
        )

    # save the dataframe with proper name
    response_dataframe = DataFrame(response_list)

    submit_time = get_current_time()

    # save it to proper folder
    response_dataframe.to_csv(
        destination_folder / f"response_{submit_time}.csv", index=False
    )


if __name__ == "__main__":
    main()
