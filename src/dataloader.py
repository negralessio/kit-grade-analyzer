import tabula
import logging
import pandas as pd

from typing import Optional

logger = logging.getLogger(__name__)


class DataLoader:

    def __init__(self, url: str):
        self.url: str = url.strip()
        self.study = None
        self.df = None

        self._set_study()

    def load_data(self) -> None:
        df_list = tabula.read_pdf(self.url, pages='all')
        self.df = df_list[0].iloc[:, 1:]
        self._preprocess_df()

    def _preprocess_df(self) -> None:
        self.df["Note"] = self.df["Note"].str.replace(',', '.').astype(float)
        self.df["Prozent"] = self.df["Prozent"].str.replace(',', '.').astype(float)
        self.df["Kumuliert"] = self.df["Kumuliert"].str.replace(',', '.').astype(float)

    def get_df(self) -> pd.DataFrame:
        if self.df is not None:
            return self.df
        else:
            raise ValueError("Call 'load_data()' first.")

    def _set_study(self):
        self.study = self.url.split("ECTS_Tab_")[1].split(".pdf")[0]

    def get_study(self) -> Optional[str]:
        if self.study is not None:
            return self.study
        else:
            return None
