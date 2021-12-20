from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

from torch.utils.data import DataLoader, random_split
from torchvision.datasets import MNIST
import os
from torchvision import transforms
from pytorch_lightning import Trainer, LightningDataModule

from module import ThreeLinearLayerClassifier


class MNISTDataModule(LightningDataModule):
    def __init__(self, data_dir: Path):
        super().__init__()
        self.data_dir = data_dir
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    def prepare_data(self):
        # called only on 1 GPU
        MNIST(os.getcwd(), train=True, download=True)
        MNIST(os.getcwd(), train=False, download=True)

    def setup(self, stage: Optional[str] = None):
        # called on every GPU
        if stage == "fit" or stage is None:
            mnist_full = MNIST(str(self.data_dir), train=True, transform=self.transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        if stage == "test" or stage is None:
            self.mnist_test = MNIST(str(self.data_dir), train=False, transform=self.transform)

        if stage == "predict" or stage is None:
            self.mnist_predict = MNIST(str(self.data_dir), train=False, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=32)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=32)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=32)

DATA_DIR = Path.home() / "data" / "mnist"


def parse_args():
    parser = ArgumentParser()
    parser = ThreeLinearLayerClassifier.add_model_specific_args(parser)
    parser = Trainer.add_argparse_args(parser)

    return parser.parse_args()


def train_via_data_module():
    args = parse_args()
    mnist_dm = MNISTDataModule(DATA_DIR)
    model = ThreeLinearLayerClassifier()
    trainer = Trainer.from_argparse_args(args)
    trainer.fit(model, mnist_dm.train_dataloader())


def train_with_validation_step():
    args = parse_args()
    mnist_dm = MNISTDataModule(DATA_DIR / "mnist")
    model = ThreeLinearLayerClassifier()
    trainer = Trainer.from_argparse_args(args)
    trainer.fit(model, mnist_dm.train_dataloader(), mnist_dm.val_dataloader())


def train_on_gpu():
    args = parse_args()
    mnist_dm = MNISTDataModule(DATA_DIR / "mnist")
    model = ThreeLinearLayerClassifier(args)
    trainer = Trainer.from_argparse_args(args, gpus=1)
    trainer.fit(model, mnist_dm)


def train_without_data_module():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    mnist_train = MNIST(str(DATA_DIR), train=True, download=True, transform=transform)
    mnist_train = DataLoader(mnist_train, batch_size=64)

    model = ThreeLinearLayerClassifier()
    trainer = Trainer()
    trainer.fit(model, mnist_train)