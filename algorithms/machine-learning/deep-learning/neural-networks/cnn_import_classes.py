"""
Convolutional Neural Network in Raw Python (with Numpy, implemented using im2col)

Not self-contained: imports classes and methods from `layers`.

Adapted from CS231n http://cs231n.github.io/neural-networks-case-study/

Jessica Yung
Jan 2018
"""
import numpy as np
import matplotlib.pyplot as plt
from layers import fc2d, relu, softmax_loss
from cnn_class import cnn2d
from data import generate_spiral_data
import pickle


###########################
# TODO: set model parameters
###########################

# Parameters
# regularisation strength
reg = 1e-3
# Parameter update step size
step_size = 1e-0
# Number of training epochs
n_epochs = 10
# Size of hidden layer
h1_units = 32
f1_field = 3

###########################
# Import MNIST dataset
###########################
with open('mnist100.pickle', 'rb') as f:
    X_train, y_train, X_test, y_test = pickle.load(f)

# Number of classes
K = 10
# Dimensions of input
num_examples, Xh, Xw = X_train.shape
Xd = 1

###########################
# Multilayer Perceptron classifier
###########################

# Initialise parameters
cnn1 = cnn2d(input_shape=(Xh,Xw,Xd), filter_shape=(f1_field, f1_field), num_filters=h1_units)
def flatten(x, n_examples):
    return np.reshape(x, (n_examples,-1))
relu1 = relu()
fc2 = fc2d(cnn1.yw*cnn1.yh*Xd*h1_units, K)
data_loss_fn = softmax_loss(y_train)

for i in range(n_epochs):
    # Forward pass
    conv1 = cnn1.forward(X_train)
    print("conv1:", conv1.shape)
    flatten1 = flatten(conv1, num_examples)
    h1 = relu1.forward(flatten1)
    scores = fc2.forward(h1)
    data_loss = data_loss_fn.forward(scores)
    reg_loss = 0.5*reg*(np.sum(cnn1.W * cnn1.W) + np.sum(fc2.W*fc2.W))
    loss = data_loss + reg_loss
    if i % 1 == 0:
        print("Epoch: %d, Loss: %f" % (i, loss))

    # Backprop
    # dLi/dfk = pk - 1(yi=k)
    dscores = data_loss_fn.backward()
    # print("dscores:",dscores.shape)
    dh1 = fc2.backward(dscores)
    # print("dh1:",dh1.shape)
    dconv1 = relu1.backward(dh1)
    # print("dconv1:",dconv1.shape)
    dconv1 = np.reshape(dconv1, (num_examples, cnn1.yh, cnn1.yw, cnn1.num_filters))
    dX = cnn1.backward(dconv1)
    # print(dX.shape)
    # TODO: do we need to take the mean of the gradients? Or is this included in the learning rate (which should then take into account batch size?) I think it's already taken into account.

    # Gradient from regularisation
    # print("cnn1.dW:",cnn1.dW.shape)
    # print("cnn1.W:",cnn1.W.shape)
    cnn1.dW += reg*cnn1.W
    fc2.dW += reg*fc2.W

    # Parameter update
    for i in range(num_examples):
        cnn1.W += -step_size * cnn1.dW[i]
        # print("cnn1.b:",cnn1.b.shape)
        # print("cnn1.db:",cnn1.db.shape)
        cnn1.b += -step_size * cnn1.db[i]
    fc2.W += -step_size * fc2.dW
    fc2.b += -step_size * fc2.db

print("cnn1.W: ", cnn1.W.shape)
# Evaluate training set accuracy
conv1 = cnn1.forward(X_train)
print("conv1: ", conv1.shape)
print("conv1: ", conv1[0])
h1_prod = flatten(conv1,num_examples)
h1 = relu1.forward(h1_prod)
scores = fc2.forward(h1)
predicted_class = np.argmax(scores, axis=1)
print("Training accuracy: %.2f" % (np.mean(predicted_class == y_train)))

exp_scores = np.exp(scores)
probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True) # sum along each row
print(probs.shape)
print(probs[:2])
# TODO: plot results

# TODO: split into training and validation sets

# TODO: plot training vs validation loss
