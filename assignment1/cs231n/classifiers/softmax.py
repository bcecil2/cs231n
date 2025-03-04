from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    numExamples = X.shape[0]
    numClasses = W.shape[1]
    numDim = X.shape[0]
    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    for i in range(numExamples):
        scores = X[i]@W
        scores -= np.max(scores)
        correct = scores[y[i]]
        loss += -correct + np.log(np.sum(np.exp(scores)))
        for k in range(numClasses):
            norm = np.exp(scores[k])/np.sum(np.exp(scores))
            dW[:,k] += (norm - (y[i] == k))*X[i]

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    loss /= numExamples
    loss += reg*0.5*np.sum(np.square(W))
                                                
    dW /= numExamples
    dW += reg*W            
    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    numExamples = X.shape[0]
    numClasses = W.shape[1]
    numDim = X.shape[0]
    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    exps = X@W
    exps = exps - np.max(exps,axis=1,keepdims=True)
    exps = np.exp(exps)
    nums = exps[range(numExamples),y]
    sums = np.sum(exps,axis = 1)
    loss = np.sum(-np.log(nums/sums))
    loss /= numExamples
    loss += reg*0.5*np.sum(np.square(W))
    
    exps = exps/np.sum(exps,axis=1,keepdims=True)
    exps[range(numExamples),y] -= 1
    dW = X.T@exps
    dW /= numExamples
    dW += reg*W 
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
