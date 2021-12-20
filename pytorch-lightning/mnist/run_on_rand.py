import torch

from module import ThreeLinearLayerClassifier

net = ThreeLinearLayerClassifier()
x = torch.randn(1, 1, 28, 28)
out = net(x)
print(out.shape)