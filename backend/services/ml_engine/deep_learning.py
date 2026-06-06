import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, r2_score


class FeedForwardNet(nn.Module):
    # simple fully connected network, works for tabular data
    def __init__(self, input_dim: int, hidden_dims: list, output_dim: int, dropout: float = 0.3):
        super().__init__()
        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = hidden_dim

        layers.append(nn.Linear(prev_dim, output_dim))
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)


def train_neural_network(
    X: pd.DataFrame,
    y: pd.Series,
    problem_type: str,
    epochs: int = 50,
    batch_size: int = 32,
    learning_rate: float = 0.001
) -> dict:

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"training neural network on {device}")

    X_np = X.values.astype(np.float32)
    input_dim = X_np.shape[1]

    # encode target for classification
    if problem_type == "classification":
        le = LabelEncoder()
        y_np = le.fit_transform(y).astype(np.int64)
        output_dim = len(np.unique(y_np))
        criterion = nn.CrossEntropyLoss()
    else:
        y_np = y.values.astype(np.float32)
        output_dim = 1
        criterion = nn.MSELoss()

    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_np, y_np, test_size=0.2, random_state=42
    )

    # tensors
    X_train_t = torch.FloatTensor(X_train).to(device)
    y_train_t = torch.LongTensor(y_train).to(device) if problem_type == "classification" else torch.FloatTensor(y_train).to(device)
    X_test_t = torch.FloatTensor(X_test).to(device)

    dataset = TensorDataset(X_train_t, y_train_t)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # build model
    hidden_dims = [128, 64, 32]
    model = FeedForwardNet(input_dim, hidden_dims, output_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)

    # training loop
    train_losses = []
    model.train()

    for epoch in range(epochs):
        epoch_loss = 0
        for X_batch, y_batch in loader:
            optimizer.zero_grad()
            output = model(X_batch)

            if problem_type == "regression":
                output = output.squeeze()

            loss = criterion(output, y_batch)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        scheduler.step()
        avg_loss = epoch_loss / len(loader)
        train_losses.append(round(avg_loss, 4))

        if (epoch + 1) % 10 == 0:
            print(f"epoch {epoch+1}/{epochs} — loss: {avg_loss:.4f}")

    # evaluate
    model.eval()
    with torch.no_grad():
        test_output = model(X_test_t)

        if problem_type == "classification":
            preds = torch.argmax(test_output, dim=1).cpu().numpy()
            score = round(accuracy_score(y_test, preds), 4)
            metric_name = "accuracy"
        else:
            preds = test_output.squeeze().cpu().numpy()
            score = round(r2_score(y_test, preds), 4)
            metric_name = "r2_score"

    return {
        "model": "Neural Network (PyTorch)",
        metric_name: score,
        "final_loss": train_losses[-1],
        "epochs_trained": epochs,
        "architecture": f"Input({input_dim}) → 128 → 64 → 32 → Output({output_dim})",
        "device": str(device),
        "train_losses": train_losses[::5],  # every 5th loss to keep it small
    }