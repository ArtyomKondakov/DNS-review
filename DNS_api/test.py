import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import torch
import seaborn as sns
import transformers as ppb
import warnings
warnings.filterwarnings('ignore')
df = pd.read_excel('main.xlsx')
df = df.dropna().drop_duplicates()
df = df[['review','Unnamed: 2']]
df = df.where(df.values != 'качественный това').dropna()
df = df.where(df.values != 'некачественный това').dropna()
df = df.reset_index().drop('index', axis=1)
df['review'] = df['review'].str.lower()
df['Unnamed: 2'].value_counts()
df.rename(columns={'review':0,'Unnamed: 2':1}, inplace=True)
df = df[[0,1]]
df[0] = df[0].str[:70]
batch_1 = df
# For DistilBERT:
model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')

## Want BERT instead of distilBERT? Uncomment the following line:
#model_class, tokenizer_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')

# Load pretrained model/tokenizer
tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
model = model_class.from_pretrained(pretrained_weights)

import joblib
filename = 'ml_model/tokenizer.sav'
joblib.dump(tokenizer, filename)

import joblib
filename = 'ml_model/model.sav'
joblib.dump(model, filename)


tokenized = batch_1[0].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))
max_len = 0
for i in tokenized.values:
    if len(i) > max_len:
        max_len = len(i)

padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])
attention_mask = np.where(padded != 0, 1, 0)
input_ids = torch.tensor(padded)
input_ids = torch.tensor(padded).to(torch.int64)
attention_mask = torch.tensor(attention_mask).to(torch.int64)

with torch.no_grad():
    last_hidden_states = model(input_ids, attention_mask=attention_mask)
features = last_hidden_states[0][:,0,:].numpy()
labels = batch_1[1]
train_features, test_features, train_labels, test_labels = train_test_split(features, labels)
from imblearn.over_sampling import SMOTE
import seaborn as sns
smote = SMOTE(random_state=2)
X_train_s, y_train_s = smote.fit_sample(train_features, train_labels.ravel())


sns.countplot(x = y_train_s, data = df)
from xgboost import XGBClassifier

# создание переменной бустинга
xgmodel = XGBClassifier(iterations=500,
                        learning_rate=1,
                        depth=6)
# Обучение модели
xgmodel.fit(X_train_s, y_train_s, verbose=False)
# Предсказание на тестовой выборке
xgpreds = xgmodel.predict(test_features)
import joblib
filename = 'dns.sav'
joblib.dump(xgmodel, filename)

