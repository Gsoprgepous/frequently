# -*- coding: utf-8 -*-
"""Копия блокнота "Untitled0.ipynb"

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fMBFBq6RJ5InvbmXQ_AloKUKOon4GJU4
"""

import pandas as pd

# Создаем простой датасет
data = {
    'text': [
        "я так счастлив!)))",
        "у меня хорошее настроение!",
        "сегодня не очень хороший день(",
        "как же я вас люблю!",
        "он меня не слышит...",
        "это просто потрясающе!!!",
        "у меня плохое предчувствие((",
        "все будет хорошо)",
        "надо было поосторожнее...",
        "мне грустно(",
        "я в большом восторге!!",
        "ты молодец!!",
        "сегодня был ужасный день((",
        "какие вы крутые!",
        "я не справилась...",
        "это просто невероятно!",
        "очень грустно ((",
        "у меня все супер)",
        "надо было думать...",
        "чувствую себя не очень(",
        "мне очень весело!!"

    ],
    'emotion': [
        "сильная радость",
        "восхищение",
        "грусть",
        "сильная радость",
        "разочарование",
        "восхищение",
        "огромная грусть",
        "просто позитивный настрой",
        "разочарование",
        "грусть",
        "сильная радость",
        "восхищение",
        "грусть",
        "сильная радость",
        "разочарование",
        "восхищение",
        "огромная грусть",
        "просто позитивный настрой",
        "разочарование",
        "грусть",
        "сильная радость"

    ]
}

df = pd.DataFrame(data)

# Сохранение датасета в CSV файл
df.to_csv('emotions_dataset.csv', index=False)

!pip install transformers

from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader

# Загрузка токенизатора и модели
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(emotion_labels))

# Применение токенизации
X_encoded = tokenizer(X.tolist(), padding=True, truncation=True, return_tensors='pt')

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from keras.utils import to_categorical
import numpy as np

# Разделение данных на трейн и тест
X = df['text']
y = df['emotion']

# Преобразуем метки эмоций в числовые значения
emotion_labels = {label: idx for idx, label in enumerate(set(y))}
y = np.array([emotion_labels[label] for label in y])
y = to_categorical(y)  # Преобразуем в one-hot encoding

# Векторизация текста
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X).toarray()

# Разделяем на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

from keras.models import Sequential
from keras.layers import Dense

# Создаем модель нейросети
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(emotion_labels), activation='softmax'))  # выходной слой для классификации эмоций

# Компилируем модель
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Обучаем модель
model.fit(X_train, y_train, epochs=100, batch_size=5, validation_data=(X_test, y_test))

# Установка библиотеки transformers, если она еще не установлена
!pip install transformers

# Импорт необходимых классов
from transformers import TrainingArguments, Trainer

# Создание объекта TrainingArguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy="epoch",
    logging_dir='./logs',
)

# Оценка модели
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Потери: {loss}, Точность: {accuracy}')

def predict_emotion(text):
    vectorized_text = vectorizer.transform([text]).toarray()
    prediction = model.predict(vectorized_text)
    predicted_emotion = np.argmax(prediction)
    return list(emotion_labels.keys())[predicted_emotion]

# Пример использования
print(predict_emotion("грустно("))  # Прогнозируем эмоцию