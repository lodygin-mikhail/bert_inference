import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from logger import get_logger

logger = get_logger(__name__)

class BertModel:
    """
    Модель для анализа тональности текста с использованием BERT.
    """
    def __init__(self, model_name:str="cointegrated/rubert-tiny-sentiment-balanced"):
        """
        Инициализирует модель и токенизатор.
        :param model_name: Название модели из HuggingFace Hub.
            По умолчанию 'cointegrated/rubert-tiny-sentiment-balanced'.
        """
        logger.info("Инициализация модели: %s", model_name)
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.eval()
            logger.debug("Модель загружена успешно")
        except Exception as e:
            logger.error("Ошибка загрузки модели: %s", e, exc_info=True)
            raise

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if not torch.cuda.is_available():
            logger.warning("Используется CPU вместо GPU")
        self.model.to(self.device)
        logger.debug("Модель загружена в память")

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Предсказывает тональность для списка текстов.
        :param data: pd.DataFrame
        :return: pd.DataFrame с полученными скорами тональности от -1 до 1
        """
        logger.info("Начало инференса модели")
        with torch.no_grad():
            texts = data['review'].tolist()
            logger.debug("Предсказание для текста длиной %d символов", len(texts))

            try:
                inputs = self.tokenizer(texts,
                                        return_tensors='pt',
                                        truncation=True,
                                        padding=True)
                output = self.model(**inputs).logits
                proba = torch.sigmoid(output)
                proba = proba.cpu()

                scores = proba.matmul(torch.Tensor([-1, 0, 1]))
                data['scores'] = scores.round(decimals=2)
                logger.info("Успешно обработано %d отзывов", len(data))
                logger.debug("Предсказание завершено: %s")
                return data

            except Exception as e:
                logger.error("Ошибка предсказания: %s", e, exc_info=True)
            raise

