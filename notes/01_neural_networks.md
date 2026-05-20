# Neural Networks

A neural network is a parameterized function approximator built from layers of simple computational units called neurons. Each neuron computes a weighted sum of its inputs, adds a bias term, and passes the result through a nonlinear activation function. By stacking many such layers, neural networks can represent extremely complex mappings between inputs and outputs.

## Structure

A feedforward neural network is organized into three kinds of layers:

- **Input layer**: receives the raw features (e.g. pixel values, token embeddings).
- **Hidden layers**: perform intermediate transformations. The "depth" of the network refers to the number of hidden layers.
- **Output layer**: produces the final prediction (a class label, a regression value, or a probability distribution).

A single neuron computes `y = f(w · x + b)` where `w` is the weight vector, `b` is the bias, `x` is the input, and `f` is the activation function.

## Activation Functions

Without nonlinear activations, a stack of layers would collapse into a single linear transformation. Common activations include:

- **ReLU** (`max(0, x)`): the default for hidden layers. Cheap, sparse, and avoids vanishing gradients for positive inputs.
- **Sigmoid** (`1 / (1 + e^-x)`): squashes outputs to (0, 1). Used historically but suffers from saturation.
- **Tanh**: like sigmoid but centered at zero, range (-1, 1).
- **Softmax**: used in the output layer for multiclass classification; converts logits into a probability distribution.
- **GELU**: smooth approximation of ReLU, common in transformer architectures.

## Universal Approximation

The universal approximation theorem states that a feedforward network with a single hidden layer and a nonlinear activation can approximate any continuous function on a compact domain, given enough neurons. In practice, **deep** networks (many layers) are far more parameter-efficient than wide shallow networks because they can compose hierarchical features.

## Training

Training a neural network means finding weight values that minimize a loss function over a dataset. This is done with gradient-based optimization (see [Gradient Descent](03_gradient_descent.md)) where gradients are computed via [Backpropagation](02_backpropagation.md). The choice of architecture, loss function, optimizer, and regularization strategy all materially affect generalization.
