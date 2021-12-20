from torch.nn import functional as F
from torch import nn
from torch.optim import Adam
from pytorch_lightning.core.lightning import LightningModule


class ThreeLinearLayerClassifier(LightningModule):
    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = parent_parser.add_argument_group("ThreeLinearLayerClassifier")
        parser.add_argument("--layer_1_dim", type=int, default=128)
        parser.add_argument("--learning_rate", type=float, default=1e-3)
        return parent_parser

    def __init__(self, layer_1_dim: int, learning_rate: float):
        super().__init__()

        # mnist images are (1, 28, 28) (channels, height, width)
        self.layer_1 = nn.Linear(28 * 28, layer_1_dim)
        self.layer_2 = nn.Linear(128, 256)
        self.layer_3 = nn.Linear(256, 10)

        self._learning_rate = learning_rate

        self.save_hyperparameters()

    def configure_optimizers(self):
        return Adam(self.parameters(), lr=self._learning_rate)

    def _loss(self, x, y):
        logits = self(x)
        return F.nll_loss(logits, y)

    def training_step(self, batch, batch_idx):
        x, y = batch
        loss = self._loss(x, y)
        self.log("loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        loss = self._loss(x, y)
        self.log("val_loss", loss)

    def forward(self, x):
        batch_size, channels, height, width = x.size()

        # (b, 1, 28, 28) -> (b, 1*28*28)
        x = x.view(batch_size, -1)
        x = self.layer_1(x)
        x = F.relu(x)
        x = self.layer_2(x)
        x = F.relu(x)
        x = self.layer_3(x)

        x = F.log_softmax(x, dim=1)
        return x