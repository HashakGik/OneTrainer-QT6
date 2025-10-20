# TODO: after pull request is accepted, move this into modules.util.enum

from enum import Flag, auto
from modules.util.enum.TrainingMethod import TrainingMethod

class ModelFlags(Flag):
    NONE = 0  # Invalid initial value.
    UNET = auto()
    PRIOR = auto()
    OVERRIDE_PRIOR = auto()
    OVERRIDE_TE4 = auto()
    TE1 = auto()
    TE2 = auto()
    TE3 = auto()
    TE4 = auto()
    VAE = auto()
    EFFNET = auto()
    DEC = auto()
    DEC_TE = auto()
    ALLOW_SAFETENSORS = auto()
    ALLOW_DIFFUSERS = auto()
    ALLOW_LEGACY_SAFETENSORS = auto()

    @staticmethod
    def getFlags(model_type, training_method):
        flags = ModelFlags.NONE

        if model_type.is_stable_diffusion():  # TODO simplify
            flags = ModelFlags.UNET | ModelFlags.TE1 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method in [TrainingMethod.FINE_TUNE, TrainingMethod.FINE_TUNE_VAE]:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_stable_diffusion_3():
            flags = ModelFlags.PRIOR | ModelFlags.TE1 | ModelFlags.TE2 | ModelFlags.TE3 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_stable_diffusion_xl():
            flags = ModelFlags.UNET | ModelFlags.TE1 | ModelFlags.TE2 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_wuerstchen():
            flags = ModelFlags.PRIOR | ModelFlags.TE1
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method != TrainingMethod.FINE_TUNE or model_type.is_stable_cascade():
                flags |= ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_pixart():
            flags = ModelFlags.PRIOR | ModelFlags.TE1 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_flux():
            flags = ModelFlags.PRIOR | ModelFlags.OVERRIDE_PRIOR | ModelFlags.TE1 | ModelFlags.TE2 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_chroma():
            flags = ModelFlags.PRIOR | ModelFlags.OVERRIDE_PRIOR | ModelFlags.TE1 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_qwen():
            flags = ModelFlags.PRIOR | ModelFlags.OVERRIDE_PRIOR | ModelFlags.TE1 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_sana():
            flags = ModelFlags.PRIOR | ModelFlags.TE1 | ModelFlags.VAE
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            else:
                flags |= ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_hunyuan_video():
            flags = ModelFlags.PRIOR | ModelFlags.TE1 | ModelFlags.TE2 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        elif model_type.is_hi_dream():
            flags = ModelFlags.PRIOR | ModelFlags.OVERRIDE_TE4 | ModelFlags.TE1 | ModelFlags.TE2 | ModelFlags.TE3 | ModelFlags.TE4 | ModelFlags.VAE | ModelFlags.ALLOW_SAFETENSORS
            if training_method == TrainingMethod.FINE_TUNE:
                flags |= ModelFlags.ALLOW_DIFFUSERS
            if training_method == TrainingMethod.LORA:
                flags |= ModelFlags.ALLOW_LEGACY_SAFETENSORS

        return flags