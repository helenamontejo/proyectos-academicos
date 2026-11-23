# PG1: predicción de contratación de depósitos a plazo

Práctica grupal de aprendizaje automático. Es un problema de clasificación binaria muy desbalanceado (11,23 % de positivos) sobre datos de marketing bancario. La métrica es Macro F1 y no se usa la variable `duration`, por fuga de información.

## Contenido
- `codigo.ipynb`: análisis exploratorio, preprocesamiento con `Pipeline`, validación (hold-out y CV estratificada), comparativa de KNN, árbol de decisión, bagging, Random Forest, Extra Trees y AdaBoost, y resultados en Kaggle.

## Resultados
Mejor puntuación privada en Kaggle: 0,6870 (árbol de decisión optimizado con umbral 0,73).

## Datos
Los datos (`train.csv`, `test_nolabel.csv`, `sample_submission.csv`) no se incluyen porque son material de la asignatura. Para ejecutar el cuaderno, colócalos en la misma carpeta.

## Autoría
Trabajo realizado en grupo por Helena Montejo, Icíar Guerrero, Belén Tejido y Flavia Buitrón.
