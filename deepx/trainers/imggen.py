import math
import warnings

import torch
from lightning import LightningDataModule, LightningModule
from torch import nn, optim

from .trainer import TrainerX


class ImageGenerationTrainer(TrainerX):
    NAME = "imagegeneration"

    def __init__(
        self,
        model: str | LightningModule,
        datamodule: str | LightningDataModule,
        batch_size: int = 32,
        train_ratio: float = 0.8,
        num_workers: int = 2,
        download: bool = False,
        lr: float = 1e-3,
        beta1: float = 0.9,
        beta2: float = 0.999,
        loss_fn: str | nn.Module = "bce",
        optimizer: str | optim.Optimizer = "adam",
        scheduler: str | optim.lr_scheduler._LRScheduler = "cos",
        root_dir: str = "/workspace",
        data_dir: str = "/workspace/experiments/data",
        log_dir: str = "/workspace/experiments/mlruns",
        negative_slope: float = 0.01,
        dropout: float = 0.0,
        latent_dim: int = 1024,
        base_dim_g: int = 128,
        base_dim_d: int = 128,
        **kwargs,
    ):
        super().__init__(
            model=model,
            datamodule=datamodule,
            batch_size=batch_size,
            train_ratio=train_ratio,
            num_workers=num_workers,
            download=download,
            lr=lr,
            beta1=beta1,
            beta2=beta2,
            loss_fn=loss_fn,
            optimizer=optimizer,
            scheduler=scheduler,
            root_dir=root_dir,
            data_dir=data_dir,
            log_dir=log_dir,
            **kwargs,
        )

        if loss_fn != "bce":
            warnings.warn(
                f"Loss function {loss_fn} might cause problems. Use 'bce' instead."
            )

        # self.dm_cfg.update({})
        self.datamodule = self.get_datamodule(datamodule=datamodule, **self.dm_cfg)

        h, w = self.datamodule.SIZE
        tgt_shape = (self.datamodule.NUM_CHANNELS, h, w)
        self.model_cfg.update(
            {
                "tgt_shape": tgt_shape,
                "negative_slope": negative_slope,
                "dropout": dropout,
                "latent_dim": latent_dim,
                "base_dim_g": base_dim_g,
                "base_dim_d": base_dim_d,
            }
        )
        self.model = self.get_model(model, **self.model_cfg)

        self.algo_cfg.update({"model": self.model})
        self.algo = self.get_algo(algo=self.NAME, **self.algo_cfg)

        self.hparams.update(self.dm_cfg)
        self.hparams.update(self.model_cfg)
        self.hparams.update(self.algo_cfg)
