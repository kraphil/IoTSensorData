# -*- coding: utf-8 -*-
"""AutoencoderAU.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SXPRPVvaM2RTWmKzC-p8fJkysxgWL1kQ
"""



import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, recall_score, accuracy_score, precision_score
from tensorflow.keras.optimizers import SGD, RMSprop, Adam


RANDOM_SEED = 2021 
TEST_PCT = 0.1
LABELS = ["Normal","Anomaly"]

print(tf.__version__)

dataset = pd.read_csv("experiment_orderedLabels.csv")
dataset = dataset.drop('Machining_Process', 1)
dataset = dataset.drop('Z1_CurrentFeedback', 1)
dataset = dataset.drop('Z1_DCBusVoltage', 1)

dataset.head()

# Encode a numeric column as zscores
def encode_numeric_zscore(dataset, name, mean=None, sd=None):
    if mean is None:
        mean = dataset[name].mean()

    if sd is None:
        sd = dataset[name].std()

    dataset[name] = (dataset[name] - mean) / sd

def encode_text_dummy(dataset, name):
    dummies = pd.get_dummies(dataset[name])
    for x in dummies.columns:
        dummy_name = f"{name}-{x}"
        dataset[dummy_name] = dummies[x]
    dataset.drop(name, axis=1, inplace=True)

encode_numeric_zscore(dataset, 'X1_ActualPosition')
encode_numeric_zscore(dataset, 'X1_ActualVelocity')
encode_numeric_zscore(dataset, 'X1_ActualAcceleration')
encode_numeric_zscore(dataset, 'X1_CommandPosition')
encode_numeric_zscore(dataset, 'X1_CommandVelocity')
encode_numeric_zscore(dataset, 'X1_CommandAcceleration')
encode_numeric_zscore(dataset, 'X1_CurrentFeedback')
encode_numeric_zscore(dataset, 'X1_DCBusVoltage')
encode_numeric_zscore(dataset, 'X1_OutputCurrent')
encode_numeric_zscore(dataset, 'X1_OutputVoltage')
encode_numeric_zscore(dataset, 'X1_OutputPower')
encode_numeric_zscore(dataset, 'Y1_ActualPosition')
encode_numeric_zscore(dataset, 'Y1_ActualVelocity')
encode_numeric_zscore(dataset, 'Y1_ActualAcceleration')
encode_numeric_zscore(dataset, 'Y1_CommandPosition')
encode_numeric_zscore(dataset, 'Y1_CommandVelocity')
encode_numeric_zscore(dataset, 'Y1_CommandAcceleration')
encode_numeric_zscore(dataset, 'Y1_CurrentFeedback')
encode_numeric_zscore(dataset, 'Y1_DCBusVoltage')
encode_numeric_zscore(dataset, 'Y1_OutputCurrent')
encode_numeric_zscore(dataset, 'Y1_OutputVoltage')
encode_numeric_zscore(dataset, 'Y1_OutputPower')
encode_numeric_zscore(dataset, 'Z1_ActualPosition')
encode_numeric_zscore(dataset, 'Z1_ActualVelocity')
encode_numeric_zscore(dataset, 'Z1_ActualAcceleration')
encode_numeric_zscore(dataset, 'Z1_CommandPosition')
encode_numeric_zscore(dataset, 'Z1_CommandVelocity')
encode_numeric_zscore(dataset, 'Z1_CommandAcceleration')
#encode_numeric_zscore(dataset, 'Z1_CurrentFeedback')
#encode_numeric_zscore(dataset, 'Z1_DCBusVoltage')
encode_numeric_zscore(dataset, 'Z1_OutputVoltage')
encode_numeric_zscore(dataset, 'S1_ActualPosition')
encode_numeric_zscore(dataset, 'S1_ActualVelocity')
encode_numeric_zscore(dataset, 'S1_ActualAcceleration')
encode_numeric_zscore(dataset, 'S1_CommandPosition')
encode_numeric_zscore(dataset, 'S1_CommandVelocity')
encode_numeric_zscore(dataset, 'S1_CommandAcceleration')
encode_numeric_zscore(dataset, 'S1_CurrentFeedback')
encode_numeric_zscore(dataset, 'S1_DCBusVoltage')
encode_numeric_zscore(dataset, 'S1_OutputCurrent')
encode_numeric_zscore(dataset, 'S1_OutputVoltage')
encode_numeric_zscore(dataset, 'S1_OutputPower')
encode_numeric_zscore(dataset, 'S1_SystemInertia')
encode_numeric_zscore(dataset, 'M1_CURRENT_PROGRAM_NUMBER')
encode_numeric_zscore(dataset, 'M1_sequence_number')
encode_numeric_zscore(dataset, 'M1_CURRENT_FEEDRATE')
#encode_text_dummy(dataset, 'Machining_Process')

dataset.head()

dataset.isna().sum()

#check for any  nullvalues 
print("Any nulls in the dataset ",dataset.isnull().values.any() )
print('-------')
print("No. of unique labels ", len(dataset['Label'].unique()))
#print("Label values ",dataset.Class.unique())
#0 is for normal sensor data
#1 is for fraudulent sensor data
print('-------')
print("Break down of the Normal and Fraud Sensor Data")
print(pd.value_counts(dataset['Label'], sort = True) )

#Visualizing the imbalanced dataset
count_classes = pd.value_counts(dataset['Label'], sort = True)
count_classes.plot(kind = 'bar', rot=0)
plt.xticks(range(len(dataset['Label'].unique())), dataset.Label.unique())
plt.title("Frequency by observation number")
plt.xlabel("Class")
plt.ylabel("Number of Observations");

#sc=StandardScaler()
#dataset['Timestamp'] = sc.fit_transform(dataset['Timestamp'].values.reshape(-1, 1))
#dataset['Amount'] = sc.fit_transform(dataset['Amount'].values.reshape(-1, 1))

dataset.values

raw_data = dataset.values
# The last element contains if the transaction is normal which is represented by a 0 and if fraud then 1
labels = raw_data[:, -1]
data = raw_data[:, 0:-1]

train_data, test_data, train_labels, test_labels = train_test_split(
    data, labels, test_size=0.1, shuffle=False
)

labels

#test_data = tf.concat([train_data[train_labels], test_data[test_labels], test_data[~test_labels]], 0)
train_data[4]

#test_labels = np.concatenate((train_labels, test_labels, ~test_labels), axis = 0)
#test_labels

#normal_train_data = train_data[~train_labels]
#normal_train_data

#train_data = np.asarray(X).astype(np.float32)

min_val = tf.reduce_min(train_data)
max_val = tf.reduce_max(train_data)
train_data = (train_data - min_val) / (max_val - min_val)
test_data = (test_data - min_val) / (max_val - min_val)
train_data = tf.cast(train_data, tf.float32)
test_data = tf.cast(test_data, tf.float32)

train_labels = train_labels.astype(bool)
test_labels = test_labels.astype(bool)
#creating normal and fraud datasets
normal_train_data = train_data[~train_labels]
normal_test_data = test_data[~test_labels]
fraud_train_data = train_data[train_labels]
fraud_test_data = test_data[test_labels]
print(" No. of records in Fraud Train Data=",len(fraud_train_data))
print(" No. of records in Normal Train data=",len(normal_train_data))
print(" No. of records in Fraud Test Data=",len(fraud_test_data))
print(" No. of records in Normal Test data=",len(normal_test_data))

nb_epoch = 100
batch_size = 64
input_dim = normal_train_data.shape[1] #num of columns, 30
encoding_dim = 256
hidden_dim_1 = int(encoding_dim / 2) #
hidden_dim_2= int(hidden_dim_1 / 2)
learning_rate = 0.01

#input Layer
input_layer = tf.keras.layers.Input(shape=(input_dim, ))
#Encoder
encoder = tf.keras.layers.Dense(encoding_dim, activation="tanh", activity_regularizer=tf.keras.regularizers.l2(learning_rate))(input_layer)
encoder=tf.keras.layers.Dropout(0.5)(encoder)
encoder = tf.keras.layers.Dense(hidden_dim_1, activation='relu')(encoder)
encoder = tf.keras.layers.Dense(hidden_dim_2, activation='relu')(encoder) #tf.nn.leaky_relu
# Decoder
decoder = tf.keras.layers.Dense(hidden_dim_1, activation='relu')(encoder)
decoder=tf.keras.layers.Dropout(0.5)(decoder)
decoder = tf.keras.layers.Dense(encoding_dim, activation='relu')(decoder)
decoder = tf.keras.layers.Dense(input_dim, activation='sigmoid')(decoder)
#Autoencoder
autoencoder = tf.keras.Model(inputs=input_layer, outputs=decoder)
autoencoder.summary()

cp = tf.keras.callbacks.ModelCheckpoint(filepath="autoencoder.h5",
                               mode='min', monitor='val_loss', verbose=2, save_best_only=True)
# define our early stopping
#early_stop = tf.keras.callbacks.EarlyStopping(
 #   monitor='val_loss',
   # min_delta=0.0001,
  #  patience=10,
  #  verbose=1, 
  #  mode='min',
  #  restore_best_weights=True)

autoencoder.compile(metrics=['accuracy'],
                    loss='mean_squared_error', #mean_squared_error
                    optimizer='adam')

history = autoencoder.fit(normal_train_data, normal_train_data,
                    epochs=nb_epoch,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_data=(test_data, test_data),
                    verbose=1,
                    callbacks=[cp]
                    ).history

autoencoder.save("model")

plt.plot(history['loss'], linewidth=2, label='Train')
plt.plot(history['val_loss'], linewidth=2, label='Test')
plt.legend(loc='upper right')
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
#plt.ylim(ymin=0.70,ymax=1)
plt.show()

test_x_predictions = autoencoder.predict(test_data)
mse = np.mean(np.power(test_data - test_x_predictions, 2), axis=1)
error_df = pd.DataFrame({'Reconstruction_error': mse,
                        'True_class': test_labels})

#error_df.drop(error_df.loc[error_df['Reconstruction_error']>0.1].index, inplace=True)
error_df.sort_values(by=['Reconstruction_error'],ascending=False).head()
#error_df.head()

ten_percent_df = error_df.sort_values(by=['Reconstruction_error'],ascending=False)
ten_percent = ten_percent_df.head(int(len(ten_percent_df)*(10/100)))
#ten_percent = error_df.head(int(len(error_df)*(100/100)))
#threshold_fixed = ten_percent['Reconstruction_error'].mean()
threshold_fixed = ten_percent['Reconstruction_error'].mean()
print(threshold_fixed)
groups = error_df.groupby('True_class')
fig, ax = plt.subplots()

for name, group in groups:
    ax.plot(group.index, group.Reconstruction_error, marker='o', ms=3.5, linestyle='',
            label= "Fraud" if name == 1 else "Normal")
ax.hlines(threshold_fixed, ax.get_xlim()[0], ax.get_xlim()[1], colors="r", zorder=100, label='Threshold')
ax.legend()
plt.title("Reconstruction error for normal and fraud data")
plt.ylabel("Reconstruction error")
plt.xlabel("Data point index")
plt.show();

ten_percent_df = error_df.sort_values(by=['Reconstruction_error'],ascending=False)
ten_percent = ten_percent_df.head(int(len(ten_percent_df)*(10/100)))
#ten_percent = error_df.head(int(len(error_df)*(100/100)))
#threshold_fixed = ten_percent['Reconstruction_error'].mean()
threshold_fixed = ten_percent['Reconstruction_error'].mean()

#ten_percent = error_df.head(int(len(error_df)*(100/100)))
#threshold_fixed = ten_percent['Reconstruction_error'].mean()
#threshold_fixed =0.00025
pred_y = [1 if e > threshold_fixed else 0 for e in error_df.Reconstruction_error.values]
error_df['pred'] =pred_y
conf_matrix = confusion_matrix(error_df.True_class, pred_y)
plt.figure(figsize=(4, 4))
sns.heatmap(conf_matrix, xticklabels=LABELS, yticklabels=LABELS, annot=True, fmt="d");
plt.title("Confusion matrix")
plt.ylabel('True class')
plt.xlabel('Predicted class')
plt.show()

# print Accuracy, precision and recall
precision = precision_score(error_df['True_class'], error_df['pred'], average='micro')
recall = recall_score(error_df['True_class'], error_df['pred'])
F1 = 2 * (precision * recall) / (precision + recall)
print(" Accuracy: ",accuracy_score(error_df['True_class'], error_df['pred']))
print(" Recall: ",recall)
print(" Precision: ",precision)
print(" F1: ",F1)

train_data[1:2]

"""Load Model"""

from keras.models import load_model
model = load_model('autoencoder.h5', compile = True)

"""Predict"""

#input data point for prediction
data[3:4]

data_predict = train_data[1:2]
result = model.predict(data_predict)
#results of model prediction
#has to be further processed to get reconstruction error
result

tf.greater(result, .005)