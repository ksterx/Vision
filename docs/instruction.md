# Customize workflows

## Creating a new model

`<new_model>.py` should be placed in `deepx/nn/`.

```python
class NewModel(nn.Module):
    NAME = "new_model"
```

Declare your model name as `NAME = <new_model>` at the top of the class, and also add it to `registered_models` in `deepx/nn/__init__.py`.

## Creating a new task and datamodule

- `<new_task>.py` should be placed in `deepx/tasks`.

    ```python
    from .task import TaskX

    class NewTask(TaskX):
        NAME = "new_task"
    ```

- `<new_datamodule>.py` (this is for specific dataset such as `MNIST`) should be placed in `deepx/dms/data`.

    ```python
    from .dm import DataModuleX

    class NewTaskDM(DatamoduleX):
    ```

## Creating a new dataset module

`<new_dataset>.py` should be placed in `deepx/dms/data`. For example, `MNIST` is defined as follows:

```python
from deepx.tasks import ClassificationDM

class MNISTDM(ClassificationDM):
    NAME = "mnist"
```

## Creating a new trainer

`<new_trainer>.py` should be placed in `deepx/trainers/`.

```python
from .trainer import TrainerX

class NewTrainer(TrainerX):
    NAME = "new_trainer"
```

- Register your task in `deepx/tasks/__init__.py`.