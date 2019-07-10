import json
import pandas as pd


class LabelsDb:
    """
    Opens a .tsv files containing contrasts and cognitive labels, and allows to retrieve information from it, as
    well as adding new labels to existing contrasts

    Attributes
    ----------

    path: str, Default None
          Path to file

    contrast_col: str, default 'contrast'
                  Name of the column of your dataframe that contains contrast information

    sep: str, default '\t'
         Separator used in your file, to be passed to pandas

    data: pd.DataFrame
          DataFrame object containing all the information
    """

    def __init__(self, path: str = None, contrast_col: str = 'contrast', sep: str = '\t'):
        self.path = path
        if not self.path:
            self.path = self.load_config()
        self.contrast_col = contrast_col
        self.sep = sep
        self.data = pd.read_csv(self.path, sep=self.sep)

    @staticmethod
    def load_config() -> str:
        """Looks for a config file in the working directory"""
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                return config['default_path']
        except FileNotFoundError as err:
            raise FileNotFoundError(f"Path not provided and config file not found on this directory. "
                                    f"Please provide a path for your database") from err

    def get_labels(self, *contrasts: str):
        """Returns the list of labels for each passed contrast name"""
        for contrast in contrasts:
            df = self.data
            con = df[df[self.contrast_col] == contrast]

            if len(con.index) == 0:
                print(f"There is no contrast with the name {contrast}")
            else:
                labels = df.columns[con.isin([1.0]).any()]
                print(f"The labels for {contrast} are: {[label for label in labels]}")

    def add_labels(self, contrast: str, *labels: str):
        """Adds all the passed labels to the selected contrast"""
        df = self.data
        con_index = df[df[self.contrast_col] == contrast].index
        for label in labels:
            if label in df.columns:
                df.at[con_index, label] = 1.0
            else:
                print(f"There is no label with the name {label}")

    def save_db(self, path: str = None):
        if not path:
            path = self.path
        self.data.to_csv(path, sep=self.sep, index=False)
