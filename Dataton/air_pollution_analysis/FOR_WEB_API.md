## Формат входных данных
Входные данные представляют собой массив из 14 чисел, где каждое число это признак, расположенный в следующем порядке:
**'Month', 'Weekday', 'Hour', 'PT08.S1(CO)', 'C6H6(GT)', 'PT08.S2(NMHC)', 'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)', 'T', 'RH', 'AH'** <br>
Признак Month это числа от 1 до 12, признак Weekday это числа от 0 до 6


## Код для загрузки моделей:

```
import pickle

#загружаем scaler для нормализации входных данных
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

#модель линейной регрессии
with open('models\linear_model.pkl', 'rb') as file:
    model = pickle.load(file)

#модель Лассо регрессии
with open('models\lasso_model.pkl', 'rb') as file:
    model = pickle.load(file)

#модель случайного леса
with open('models\forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

#модель K-ближайших соседей
with open('models\knn_model.pkl', 'rb') as file:
    model = pickle.load(file)

#модель Support Vector Regressor
with open('models\svr_model.pkl', 'rb') as file:
    model = pickle.load(file)

#модель бустинга
with open(r'models\boosting_model.pkl', 'rb') as file:
    model = pickle.load(file)

#нейронная сеть
model = torch.load('models\nn.pt')
```
## Нормализация данных
```
normilized_data = scaler.transform(input)
```

## Использование модели для предсказания
Для всех моделей, кроме нейронной сети:
```
y_pred = model.predict(normilized_data)
```

Для нейронной сети
```
model.eval()
model.to('cpu')
y_pred = model(torch.tensor(normilized_data).to(torch.float32))
```
## Результат исследования моделей с подбором наилучших гиперпараметров
![Мое изображение](Диаграмма метркии R2 и потерь MAE.png)

## Вывод
Наилучший результат показал алгоритм SVR с метрикой R2 около 0.96. За ним идёт алгоритм KNN и градиентный бустинг.
