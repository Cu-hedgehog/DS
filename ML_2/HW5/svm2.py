from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import accuracy_score

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


def rbf(x_1, x_2, sigma=1.):
    '''Computes rbf kernel for batches of objects

    Args:
        x_1: torch.tensor shaped `(#samples_1, #features)` of type torch.float32
        x_2: torch.tensor shaped `(#samples_2, #features)` of type torch.float32
    Returns:
        kernel function values for all pairs of samples from x_1 and x_2
        torch.tensor of type torch.float32 shaped `(#samples_1, #samples_2)`
    '''
    K = np.zeros((x_1.shape[0],x_2.shape[0]))
    for i,x in enumerate(x_1):
        for j,y in enumerate(x_2):
            K[i,j] = np.exp((-1*np.linalg.norm(x-y)**2)/(2*sigma**2))
    return torch.Tensor(K).type(torch.float32)

def hinge_loss(scores, labels):
    '''Mean loss for batch of objects
    '''
    assert len(scores.shape) == 1
    assert len(labels.shape) == 1
    
    labels_ = labels.detach().numpy()
    scores_ = scores.detach().numpy()
    losses = np.maximum(0, 1 - labels_*scores_)
    return np.mean(losses)### YOUR CODE HERE


class SVM(BaseEstimator, ClassifierMixin):
    @staticmethod
    def linear(x_1, x_2):
        '''Computes linear kernel for batches of objects
        
        Args:
            x_1: torch.tensor shaped `(#samples_1, #features)` of type torch.float32
            x_2: torch.tensor shaped `(#samples_2, #features)` of type torch.float32
        Returns:
            kernel function values for all pairs of samples from x_1 and x_2
            torch.tensor shaped `(#samples_1, #samples_2)` of type torch.float32
        '''
        return torch.Tensor(np.dot(x_1, x_2.t())).type(torch.float32)### YOUR CODE HERE
    
    def __init__(
        self,
        lr: float=1e-3,
        epochs: int=2,
        batch_size: int=64,
        lmbd: float=1e-4,
        kernel_function=None,
        verbose: bool=False,
    ):
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.lmbd = lmbd
        self.kernel_function = kernel_function or SVM.linear
        self.verbose = verbose
        self.fitted = False

    def __repr__(self):
        return 'SVM model, fitted: {self.fitted}'

    def fit(self, X, Y):
        assert (np.abs(Y) == 1).all()
        n_obj = len(X)
        X, Y = torch.FloatTensor(X), torch.FloatTensor(Y)
        K = self.kernel_function(X, X).float()

        self.betas = torch.full((n_obj, 1), fill_value=0.001, dtype=X.dtype, requires_grad=True)
        self.bias = torch.zeros(1, requires_grad=True) # I've also add bias to the model
        
        optimizer = optim.SGD((self.betas, self.bias), lr=self.lr)
        for epoch in range(self.epochs):
            perm = torch.randperm(n_obj)  # Generate a set of random numbers of length: sample size
            sum_loss = 0.                 # Loss for each epoch
            for i in range(0, n_obj, self.batch_size):
                batch_inds = perm[i:i + self.batch_size]
                x_batch = X[batch_inds]   # Pick random samples by iterating over random permutation
                y_batch = Y[batch_inds]   # Pick the correlating class
                k_batch = K[batch_inds]
                
                optimizer.zero_grad()     # Manually zero the gradient buffers of the optimizer
                
                preds = k_batch @ self.betas - self.bias
                #preds = torch.sign((self.betas[batch_inds] * k_batch).sum(axis=1) + self.bias)
                #preds = k_batch @ self.betas + self.bias
                #preds = x_batch.t() @ self.betas[batch_inds] - self.bias
                #preds = self.betas[batch_inds].T @ k_batch @ self.betas - int(self.bias)### YOUR CODE HERE # get the matrix product using SVM parameters: self.betas and self.bias
                #print(max(0.1 - preds*y_batch))
                preds = preds.flatten()
                #a = hinge_loss(preds, y_batch)
                #print(preds, y_batch)
                #print(self.betas[batch_inds].shape, k_batch.shape, self.betas.shape, a, preds.shape, y_batch.shape)
                
                loss = self.lmbd * self.betas[batch_inds].T @ k_batch @ self.betas + hinge_loss(preds, y_batch)
                loss.backward()           # Backpropagation
                optimizer.step()          # Optimize and adjust weights

                sum_loss += loss.item()   # Add the loss

            if self.verbose: print("Epoch " + str(epoch) + ", Loss: " + str(sum_loss / self.batch_size))

        self.X = X
        self.fitted = True
        return self

    def predict_scores(self, batch):
        with torch.no_grad():
            batch = torch.from_numpy(batch).float()
            #print(batch.shape)
            K = self.kernel_function(batch, self.X)
            # compute the margin values for every object in the batch
            #print(self.X.shape, self.Y.shape, K.shape, self.betas.shape, self.bias.shape)
            return (K @ self.betas - self.bias).flatten()### YOUR CODE HERE

    def predict(self, batch):
        scores = self.predict_scores(batch)
        print(scores.shape)
        answers = np.full(len(batch), -1, dtype=np.int64)
        answers[scores > 0] = 1
        return answers