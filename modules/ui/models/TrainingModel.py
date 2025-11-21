from modules.ui.models.SingletonConfigModel import SingletonConfigModel
from modules.ui.models.StateModel import StateModel
from modules.ui.models.ConceptModel import ConceptModel
from modules.ui.models.SampleModel import SampleModel

from modules.trainer.CloudTrainer import CloudTrainer
from modules.trainer.GenericTrainer import GenericTrainer

from modules.zluda import ZLUDA



from modules.util.callbacks.TrainCallbacks import TrainCallbacks
from modules.util.commands.TrainCommands import TrainCommands
from modules.util.config.TrainConfig import TrainConfig

import torch
from modules.util.torch_util import torch_gc
from modules.util.TrainProgress import TrainProgress

class TrainingModel(SingletonConfigModel):
    def __init__(self, parent=None):
        self.config = None
        self.training_commands = None


    # def __training_thread_function(self):
    #     error_caught = False
    #
    #     self.training_callbacks = TrainCallbacks(
    #         on_update_train_progress=self.on_update_train_progress,
    #         on_update_status=self.on_update_status,
    #     )
    #
    #     if self.train_config.cloud.enabled:
    #         trainer = CloudTrainer(self.train_config, self.training_callbacks, self.training_commands, reattach=self.cloud_tab.reattach)
    #     else:
    #         ZLUDA.initialize_devices(self.train_config)
    #         trainer = GenericTrainer(self.train_config, self.training_callbacks, self.training_commands)
    #
    #     try:
    #         trainer.start()
    #         if self.train_config.cloud.enabled:
    #             self.ui_state.get_var("secrets.cloud").update(self.train_config.secrets.cloud)
    #         trainer.train()
    #     except Exception:
    #         if self.train_config.cloud.enabled:
    #             self.ui_state.get_var("secrets.cloud").update(self.train_config.secrets.cloud)
    #         error_caught = True
    #         traceback.print_exc()
    #
    #     trainer.end()
    #
    #     # clear gpu memory
    #     del trainer
    #
    #     self.training_thread = None
    #     self.training_commands = None
    #     torch.clear_autocast_cache()
    #     torch_gc()
    #
    #     if error_caught:
    #         self.on_update_status("error: check the console for more information")
    #     else:
    #         self.on_update_status("stopped")
    #
    #     self.training_button.configure(text="Start Training", state="normal")
    #
    # def on_update_train_progress(self, train_progress: TrainProgress, max_sample: int, max_epoch: int):
    #     self.set_step_progress(train_progress.epoch_step, max_sample)
    #     self.set_epoch_progress(train_progress.epoch, max_epoch)
    #
    # def start_training(self):
    #     if self.training_thread is None:
    #         self.save_default()
    #
    #         self.training_button.configure(text="Stop Training", state="normal")
    #
    #         self.training_commands = TrainCommands()
    #
    #         self.training_thread = threading.Thread(target=self.__training_thread_function)
    #         self.training_thread.start()
    #     else:
    #         self.training_button.configure(state="disabled")
    #         self.on_update_status("stopping")
    #         self.training_commands.stop()
    #
    # def save_default(self):
    #     self.top_bar_component.save_default()
    #     self.concepts_tab.save_current_config()
    #     self.sampling_tab.save_current_config()
    #     self.additional_embeddings_tab.save_current_config()
    #
    # def export_training(self):
    #     file_path = filedialog.asksaveasfilename(filetypes=[
    #         ("All Files", "*.*"),
    #         ("json", "*.json"),
    #     ], initialdir=".", initialfile="config.json")
    #
    #     if file_path:
    #         with open(file_path, "w") as f:
    #             json.dump(self.train_config.to_pack_dict(secrets=False), f, indent=4)
    #
    def sample_now(self):
        train_commands = self.training_commands
        if train_commands:
            train_commands.sample_default()

    def backup_now(self):
        train_commands = self.training_commands
        if train_commands:
            train_commands.backup()

    def save_now(self):
        train_commands = self.training_commands
        if train_commands:
            train_commands.save()

    def reattach(self):
        # TODO
        pass


    def train(self, progress_fn=None):
        self.progress_fn = progress_fn

        with self.critical_region():
            StateModel.instance().save_default()
            train_config = TrainConfig.default_values().from_dict(StateModel.instance().config.to_dict())

        self.training_commands = TrainCommands()

        self.training_callbacks = TrainCallbacks(
            on_update_train_progress=self.__on_update_train_progress, # NOT CALLED BY THE MODEL?
            on_update_status=self.__on_update_status,
        )

        if train_config.cloud.enabled:
            trainer = CloudTrainer(train_config, self.training_callbacks, self.training_commands, reattach=self.reattach)
        else:
            ZLUDA.initialize_devices(train_config)
            trainer = GenericTrainer(train_config, self.training_callbacks, self.training_commands)

        try:
            # TODO: if config is invalid, loops forever.
            trainer.start()
            if train_config.cloud.enabled:
                self.__on_update_secrets(train_config.secrets.cloud)
            trainer.train()
        except Exception as e:
            if train_config.cloud.enabled:
                self.__on_update_secrets(train_config.secrets.cloud)

            if self.progress_fn is not None:
                self.progress_fn({"status": "Error: check the console for more information"})
            raise e
        finally:
            trainer.end()

            # clear gpu memory
            del trainer

            self.training_commands = None
            torch.clear_autocast_cache()
            torch_gc()


    def __on_update_train_progress(self, train_progress: TrainProgress, max_sample: int, max_epoch: int):
        if self.progress_fn is not None:
            self.progress_fn({"epoch": train_progress.epoch, "max_epochs": max_epoch, "step": train_progress.step, "max_steps": max_sample})

    def __on_update_status(self, status: str):
        if self.progress_fn is not None:
            self.progress_fn({"status": status})

    def __on_reattach(self):
        pass # TODO: self.cloud_tab.reattach

        # self.reattach = True
        # try:
        #     self.parent.start_training()
        # finally:
        #     self.reattach = False

    def __on_update_secrets(self, cloud):
        pass # TODO:

    def stop_training(self):
        if self.progress_fn is not None:
            self.progress_fn({"event": "stopping"})
        if self.training_commands is not None:
            self.training_commands.stop()