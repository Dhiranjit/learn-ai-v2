# Backpropagation

Backpropagation is the algorithm used to efficiently compute the gradient of a loss function with respect to every parameter in a neural network. It is a specialized application of the chain rule of calculus, executed in reverse through the computation graph.

## The Two Passes

Training one mini-batch involves two passes:

1. **Forward pass**: inputs are propagated through the network layer by layer, producing intermediate activations and finally a prediction. The loss is computed by comparing the prediction to the target.
2. **Backward pass**: starting from the loss, gradients are propagated backwards through the graph. At each node, the local gradient is multiplied by the incoming gradient (the chain rule) to produce the gradient with respect to that node's inputs and parameters.

## The Chain Rule in Practice

If the loss `L` depends on a parameter `w` through a chain of operations `w → z → a → L`, then:

```
dL/dw = (dL/da) · (da/dz) · (dz/dw)
```

Backprop computes each of these local derivatives once and reuses them. Without this reuse, computing gradients for a network with millions of parameters would be intractable.

## Computation Graphs

Modern frameworks (PyTorch, JAX, TensorFlow) build a directed acyclic graph of operations during the forward pass. Each operation knows how to compute its local gradient. The backward pass is then a topological traversal of this graph in reverse, accumulating gradients.

## Common Issues

- **Vanishing gradients**: in deep networks with saturating activations (sigmoid, tanh), gradients can shrink to near-zero as they propagate backward, stalling learning in early layers. Mitigations: ReLU activations, residual connections, careful initialization.
- **Exploding gradients**: gradients can grow exponentially, especially in recurrent networks. Mitigated by gradient clipping and normalization.
- **Numerical stability**: operations like softmax + cross-entropy are usually fused into a single numerically stable kernel.

## Relationship to Autodiff

Backpropagation is **reverse-mode automatic differentiation** applied to scalar-valued loss functions. Reverse mode is efficient when the output is low-dimensional (a scalar loss) and the input is high-dimensional (millions of parameters) — exactly the regime of neural network training. See [Neural Networks](01_neural_networks.md) and [Gradient Descent](03_gradient_descent.md).
