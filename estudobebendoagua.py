import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Carregar os dados coletados
data = pd.read_csv('agua_data.csv')

# Separar os dados de entrada (landmarks) e os rótulos (bebendo_agua)
X = data.drop(columns=['label'])
y = data['label']

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar um classificador Random Forest
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Avaliar a acurácia do modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Acurácia: {accuracy * 100:.2f}%')

# Salvar o modelo treinado
import joblib
joblib.dump(model, 'agua_model.pkl')
