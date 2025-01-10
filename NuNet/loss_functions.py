import torch
from torch import Tensor, nn


class ModifiedMAPE(nn.Module):
    def __init__(self, **kwargs):
        super().__init__()
        self.loss_value = 0.0

    def forward(self, predictions: Tensor, ground_truths: Tensor):
        total_loss = 0.0
        epsilon = 1

        for i, (y_hat, y) in enumerate(zip(predictions, ground_truths)):
            # Calculate the absolute percentage error
            absolute_error = torch.abs(y - y_hat)
            denominator = y + epsilon

            # Calculate the mean over all elements in the tensor
            task_loss = torch.mean(absolute_error / denominator)

            total_loss += task_loss
        
        self.loss_value = total_loss
        return self.loss_value