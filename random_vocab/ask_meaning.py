import sys
from datetime import datetime
from pathlib import Path

import click
from pandas import DataFrame, read_csv

FILE_PATH = Path(__file__).resolve()
PROJECT_FOLDER = FILE_PATH.parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"
SOURCE_FILE = DATA_FOLDER / "source" / "meaning.csv"
RESULT_FOLDER = DATA_FOLDER / "result"


def crosscheck_required_vs_actual_observations(
    num_of_total_rows: int, required_rows: int
) -> int:
    return num_of_total_rows if num_of_total_rows <= required_rows else required_rows


def get_sample_dataframe(starting_alphabet, required_observation, raw_file=SOURCE_FILE):
    dataframe = read_csv(raw_file)

    if starting_alphabet:
        dataframe = dataframe[
            dataframe["word"].str.startswith(starting_alphabet, na=False)
        ]

    if dataframe.shape[0] == 0:
        print(f"No word starting with: {starting_alphabet}")
        sys.exit(1)

    sample_dataframe = dataframe.sample(
        n=crosscheck_required_vs_actual_observations(
            num_of_total_rows=dataframe.shape[0], required_rows=required_observation
        )
    )

    return sample_dataframe


def get_current_time():
    current_time = datetime.now()
    current_time_text = current_time.strftime("%Y_%m_%d_%H_%M")
    return current_time_text


@click.command()
@click.option(
    "--starting_alphabet",
    "-s",
    type=str,
    default="",
    help="Only provide words starting with particular alphabet; format: lowercase",
)
@click.option(
    "--number_of_observation",
    "-n",
    default=20,
    type=int,
    help="Provide number of questions will appear in quiz",
)
def main(starting_alphabet, number_of_observation, destination_folder=RESULT_FOLDER):
    question_bank = get_sample_dataframe(
        starting_alphabet=starting_alphabet,
        required_observation=number_of_observation,
        raw_file=SOURCE_FILE,
    )

    response_list = []
    # loop over each obsevation and ask question
    for _, row in question_bank.iterrows():
        response = click.prompt(text=row["word"], type=str)

        # save the response to dataframe for same keyword
        response_list.append(
            {"word": row["word"], "response": response, "answer": row["meaning"]}
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
