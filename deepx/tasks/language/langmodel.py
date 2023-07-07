import pathlib

import numpy as np
import torch
from lightning import LightningModule
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchmetrics.classification import MulticlassJaccardIndex
from torchtext.datasets import WikiText103
from transformers import AutoTokenizer

from deepx.nn import Transformer
from deepx.tasks import DataModule, Task


class LangModelTask(Task):
    def __init__(
        self,
        model: str | LightningModule,
        dataset_name: str,
        lr: float = 0.001,
        loss_fn: nn.Module | str = nn.CrossEntropyLoss(),
        tokenizer: str = "bert-base-uncased",
        **kwargs,
    ):
        super().__init__(model=model, dataset_name=dataset_name, lr=lr, loss_fn=loss_fn)

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self.vocab_size = self.tokenizer.vocab_size
        self.mask = None

    def training_step(self, batch, batch_idx):
        x = self.tokenizer.encode(batch, return_tensors="pt")

        logits = self(x, mask=self.mask)
        loss = self.loss_fn(logits, x)
        self.log("train_loss", loss)
        return loss


class WikiText103Dataset(Dataset):
    def __init__(self, root):
        self.train_data, self.val_data, self.test_data = WikiText103(
            root=root, split=("train", "valid", "test")
        )
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def __len__(self):
        return len(self.train_data)

    def __getitem__(self, idx):
        encoded = self.tokenizer(self.train_data[idx])
        next_token_
