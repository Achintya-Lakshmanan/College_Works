# Import libraries
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv("exams.csv")

# Encode the categorical features
le1 = LabelEncoder()
le2 = LabelEncoder()
le3 = LabelEncoder()
le4 = LabelEncoder()
le5 = LabelEncoder()

df["gender"] = le1.fit_transform(df["gender"])
df["race/ethnicity"] = le2.fit_transform(df["race/ethnicity"])
df["parental level of education"] = le3.fit_transform(df["parental level of education"])
df["lunch"] = le4.fit_transform(df["lunch"])
df["test preparation course"] = le5.fit_transform(df["test preparation course"])

# Split the dataset into features and targets
X = df.drop(["math score", "reading score", "writing score"], axis=1).values
y = df[["math score", "reading score", "writing score"]].values

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert the data to tensors
X_train = torch.from_numpy(X_train).float()
X_test = torch.from_numpy(X_test).float()
y_train = torch.from_numpy(y_train).float()
y_test = torch.from_numpy(y_test).float()

# Define the ANN model
class ANN(nn.Module):
  def __init__(self):
    super(ANN, self).__init__()
    # Define the layers and activation functions
    self.fc1 = nn.Linear(5, 20) # Input layer with 5 features and output layer with 10 neurons
    self.relu1 = nn.ReLU() # ReLU activation function for the first hidden layer
    self.fc2 = nn.Linear(20, 20) # Second hidden layer with 10 neurons and output layer with 10 neurons
    self.relu2 = nn.ReLU() # ReLU activation function for the second hidden layer
    self.fc3 = nn.Linear(20, 3) # Output layer with 10 neurons and output layer with 3 neurons (one for each score)

  def forward(self, x):
    # Define the forward pass
    out = self.fc1(x) # Pass the input through the first layer
    out = self.relu1(out) # Apply the ReLU activation function
    out = self.fc2(out) # Pass the output of the first layer through the second layer
    out = self.relu2(out) # Apply the ReLU activation function
    out = self.fc3(out) # Pass the output of the second layer through the output layer
    return out
'''
# Create an instance of the model
model = ANN()
# Define the loss function and optimizer
criterion = nn.MSELoss() # Mean squared error loss function for regression
optimizer = optim.Adam(model.parameters(), lr=0.01) # Adam optimizer with learning rate of 0.01

# Define the number of epochs for training
epochs = 100

# Train the model
for epoch in range(epochs):
  # Zero the parameter gradients
  optimizer.zero_grad()
  # Forward pass
  outputs = model(X_train)
  # Calculate the loss
  loss = criterion(outputs, y_train)
  # Backward pass and optimize
  loss.backward()
  optimizer.step()
  # Print the loss every 10 epochs
  if (epoch+1) % 10 == 0:
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# Test the model on unseen data
with torch.no_grad():
  predictions = model(X_test)
  test_loss = criterion(predictions, y_test)
  print(f"Test Loss: {test_loss.item():.4f}")

torch.save(model, 'model.pth')
torch.save(le1, 'encoder1.pkl')
torch.save(le2, 'encoder2.pkl')
torch.save(le3, 'encoder3.pkl')
torch.save(le4, 'encoder4.pkl')
torch.save(le5, 'encoder5.pkl')'''