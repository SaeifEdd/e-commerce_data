import pandas as pd


def clean(input_path: str, output_path: str):
    df = pd.read_csv(input_path)

    df.drop_duplicates(inplace=True)
    df['price'] = df['price'].str.replace('DT', '').str.replace(',', '.').astype(float)

    df.to_csv(output_path, index=False)
    return df

# next: extract more features using descriptions column