import joblib
from dns_parser import parser
import numpy as np
import torch

import pandas as pd

def model(url):
    df = parser(url)
    df = df.fillna('Нет отзывов')

    df['review'] = df['review'].str[:100]

    filename = 'ml_model/tokenizer.sav'
    tokenizer = joblib.load(filename)

    filename = 'ml_model/model.sav'
    model = joblib.load(filename)

    tokenized = df['review'].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))
    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)

    padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded).to(torch.int64)
    attention_mask = torch.tensor(attention_mask).to(torch.int64)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
    features = last_hidden_states[0][:, 0, :].numpy()

    filename = 'ml_model/dns.sav'
    xgboost = joblib.load(filename)
    result = xgboost.predict(features)
    df['pred'] = result
    return df
