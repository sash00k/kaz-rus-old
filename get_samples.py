import random
import pandas as pd


def get(df: pd.DataFrame, del_only_ru=True, del_only_kz=True, quantiles_count=100, items_in_quantile=1) -> list:
    if del_only_ru:
        df = df[df['percentage'] != 0]
    if del_only_kz:
        df = df[df['percentage'] != 1]

    boarders = df.quantile([i/quantiles_count for i in range(quantiles_count+1)])['percentage'].tolist()
    sample = []
    for i in range(quantiles_count):
        sample.extend(random.choices(df[(df['percentage']>=boarders[i]) &
                                        (df['percentage']<=boarders[i+1])]['text'].tolist(),
                                     k=items_in_quantile))
    return sample
