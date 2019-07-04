import pandas as pd


class LabelsDb:
    """
    Opens a .tsv files containing contrasts and cognitive labels, and allows to retrieve information from it, as
    well as adding new labels to existing contrasts

    Attributes
    ----------

    path: str
          Path to file

    contrast_col: str, default 'contrast'
                  Name of the column of your dataframe that contains contrast information

    sep: str, default '\t'
         Separator used in your file, to be pased to pandas

    data: pd.DataFrame
          DataFrame object containing all the information
    """

    def __init__(self, path, contrast_col='contrast', sep='\t'):
        self.path = path
        self.contrast_col = contrast_col
        self.sep = sep
        self.data = pd.read_csv(self.path, sep=self.sep)

    def get_labels(self, *contrasts):
        for contrast in contrasts:
            df = self.data
            con = df[df[self.contrast_col] == contrast]

            if len(con.index) == 0:
                print(f"There is no contrast with the name {contrast}")
            else:
                labels = df.columns[con.isin([1.0]).any()]
                print(f"The labels for {contrast} are: {[label for label in labels]}")

    def add_labels(self, contrast, *labels):
        for label in labels:
            df = self.data
            con_index = df[df[self.contrast_col] == contrast].index
            df.at[con_index, label] = 1.0
