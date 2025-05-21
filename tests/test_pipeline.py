import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from src.extract import scrape_all_pages, save_to_csv, extract_data, init_driver
from src.transform import clean
from src.load import load


class TestPipeline(unittest.TestCase):

    @patch("src.extract.scrape_page")
    @patch("src.extract.init_driver")
    def test_scrape_pages(self, fake_init_driver, fake_scrape_page):
        # create fake input functions
        fk_driver = MagicMock()
        fake_init_driver.return_value = fk_driver
        fk_df = pd.DataFrame({"col": [1]})
        fake_scrape_page.return_value = fk_df
        # call real function with fake input
        result = scrape_all_pages(2)
        # does it concatenate
        self.assertEqual(len(result), 2)
        # does it quit driver
        fk_driver.quit.assert_called_once()

    @patch("src.extract.pd.DataFrame.to_csv")
    def test_save_csv(self, mock_to_csv):
        df = pd.DataFrame({"a": [1, 2]})
        save_to_csv(df, "fake_path.csv")
        # does it call to_csv func
        mock_to_csv.assert_called_once_with("fake_path.csv", index=False)

    @patch("src.extract.scrape_all_pages")
    @patch("src.extract.save_to_csv")
    def test_extract(self, mock_save_to_csv, mock_scrape_all_pages):
        # create example df
        df = pd.DataFrame({"b": [1]})
        # make df as the return of scraping func
        mock_scrape_all_pages.return_value = df
        # apply extract with fake path
        extract_data("output.csv")

        # make sure the functions are called
        mock_scrape_all_pages.assert_called_once()
        mock_save_to_csv.assert_called_once_with(df, "output.csv")

    @patch("src.transform.pd.read_csv")
    @patch("src.transform.pd.DataFrame.to_csv")
    def test_clean(self, mock_to_csv, mock_read_csv):
        # create fake df
        mock_df = pd.DataFrame(
            {
                "price": ["1,299 DT", "1,299 DT", "999.99 DT"],
                "product": ["Phone A", "Phone A", "Phone B"],
            }
        )
        mock_read_csv.return_value = mock_df

        clean("input.csv", "output.csv")

        cleaned_df = mock_read_csv.return_value
        expected_prices = [1.299, 999.99]
        self.assertTrue(cleaned_df["price"].tolist() == expected_prices)
        self.assertEqual(len(cleaned_df), 2)

    @patch("src.load.sqlite3.connect")
    @patch("src.load.pd.read_csv")
    def test_load(self, mock_read_csv, mock_connect):
        fake_df = MagicMock()
        mock_read_csv.return_value = fake_df

        # create fake db connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # run load func
        load("fake.csv", "fake_db.db")

        fake_df.to_sql.assert_called_once_with(
            "smartphones", mock_conn, if_exists="replace", index=False
        )


if __name__ == "__main__":
    unittest.main()
