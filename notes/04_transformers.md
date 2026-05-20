# Transformers and Attention

The transformer architecture, introduced in "Attention Is All You Need" (2017), replaced recurrence with self-attention and became the foundation of modern large language models. Its key innovation is that every token in a sequence can directly attend to every other token, removing the sequential bottleneck of RNNs.

## Self-Attention

Self-attention computes a weighted combination of all tokens in a sequence for each position. For each token, three projections are computed:

- **Query (Q)**: what this token is looking for.
- **Key (K)**: what this token offers as a match.
- **Value (V)**: the actual content to aggregate.

The attention output is:

```
Attention(Q, K, V) = softmax(Q·Kᵀ / √d_k) · V
```

The scaling factor `√d_k` keeps the softmax in a numerically stable regime. The softmax over `Q·Kᵀ` produces a probability distribution: how much each token should attend to every other.

## Multi-Head Attention

Rather than one attention computation, transformers run several in parallel — each "head" learns a different relational pattern (syntactic, semantic, positional). Outputs are concatenated and linearly projected. Typical models use 8–96 heads.

## Position Encodings

Self-attention is permutation-invariant by itself. To inject order, transformers add **positional encodings** to the input embeddings — either sinusoidal (original paper), learned, or relative (e.g. RoPE in modern LLMs).

## Architecture

A transformer block consists of:

1. Multi-head self-attention
2. Residual connection + LayerNorm
3. Feedforward network (two linear layers with a nonlinearity, see [Neural Networks](01_neural_networks.md))
4. Residual connection + LayerNorm

Stacking 12–100+ such blocks yields models like BERT, GPT, T5, and Llama.

## Encoder vs Decoder

- **Encoder-only** (BERT): bidirectional self-attention, good for understanding tasks.
- **Decoder-only** (GPT, Llama): causal masked attention — each token only sees previous tokens. Used for generative LLMs.
- **Encoder-decoder** (T5, original transformer): encoder processes input; decoder generates output while attending to encoder states. Standard for translation.

## Why Transformers Won

Transformers parallelize over the sequence dimension, unlike RNNs, making them ideal for GPU training. They also scale predictably — bigger models with more data reliably yield better performance, the foundation of the modern LLM era.
