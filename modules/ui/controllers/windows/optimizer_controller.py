from PyQt6.QtWidgets import QCheckBox

from modules.ui.utils.base_controller import BaseController
from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

from modules.ui.utils.sn_line_edit import SNLineEdit
from modules.util.enum.Optimizer import Optimizer

# TODO: FOR SOME REASON THIS GIVES IMPORT ERROR (circular import: modules.optimizer.utils -> modules.utils.create -> modules.modelSetup.ChromaEmbeddingSetup -> modules.util.optimizer_util)
# from modules.util.optimizer_util import (
    # OPTIMIZER_DEFAULT_PARAMETERS,
    # #change_optimizer,
    # load_optimizer_defaults,
    # #update_optimizer_config,
# )
# TODO: for demonstration purpose, I am  temporarily copying OPTIMIZER_DEFAULT_PARAMETERS here:
OPTIMIZER_DEFAULT_PARAMETERS = {
    Optimizer.ADAFACTOR: {
        "eps": 1e-30,
        "eps2": 1e-3,
        "clip_threshold": 1.0,
        "decay_rate": -0.8,
        "beta1": None,
        "weight_decay": 0.0,
        "scale_parameter": False,
        "relative_step": False,
        "warmup_init": False,
        "stochastic_rounding": True,
        "fused_back_pass": False,
    },
    Optimizer.ADAGRAD: {
        "lr_decay": 0,
        "weight_decay": 0,
        "initial_accumulator_value": 0,
        "eps": 1e-10,
        "optim_bits": 32,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": True,
    },
    Optimizer.ADAGRAD_8BIT: {
        "lr_decay": 0,
        "weight_decay": 0,
        "initial_accumulator_value": 0,
        "eps": 1e-10,
        "optim_bits": 8,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": True,
        "fused_back_pass": False,
    },
    Optimizer.ADAM_8BIT: {
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-8,
        "weight_decay": 0,
        "amsgrad": False,
        "optim_bits": 32,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": True,
        "is_paged": False,
    },
    Optimizer.ADAMW_8BIT: {
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-8,
        "weight_decay": 1e-2,
        "amsgrad": False,
        "optim_bits": 32,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": True,
        "is_paged": False,
    },
    Optimizer.AdEMAMix_8BIT: {
        "beta1": 0.9,
        "beta2": 0.999,
        "beta3": 0.9999,
        "eps": 1e-8,
        "alpha": 5,
        "weight_decay": 1e-2,
        "min_8bit_size": 4096,
        "is_paged": False,
    },
    Optimizer.AdEMAMix: {
        "beta1": 0.9,
        "beta2": 0.999,
        "beta3": 0.9999,
        "eps": 1e-8,
        "alpha": 5,
        "weight_decay": 1e-2,
        "optim_bits": 32,
        "min_8bit_size": 4096,
        "is_paged": False,
    },
    Optimizer.ADOPT: {
        "beta1": 0.9,
        "beta2": 0.9999,
        "weight_decay": 0.0,
        "decoupled_decay": False,
        "fixed_decay": False,
        "cautious": False,
        "eps": 1e-6,
    },
    Optimizer.LAMB: {
        "bias_correction": True,
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-8,
        "weight_decay": 0,
        "amsgrad": False,
        "adam_w_mode": True,
        "optim_bits": 32,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": False,
        "max_unorm": 1.0,
    },
    Optimizer.LAMB_8BIT: {
        "bias_correction": True,
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-8,
        "weight_decay": 0,
        "amsgrad": False,
        "adam_w_mode": True,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": False,
        "max_unorm": 1.0,
    },
    Optimizer.LARS: {
        "momentum": 0,
        "dampening": 0,
        "weight_decay": 0,
        "nesterov": False,
        "optim_bits": 32,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "max_unorm": 0.02,
    },
    Optimizer.LARS_8BIT: {
        "momentum": 0,
        "dampening": 0,
        "weight_decay": 0,
        "nesterov": False,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "max_unorm": 0.02,
    },
    Optimizer.LION_8BIT: {
        "beta1": 0.9,
        "beta2": 0.999,
        "weight_decay": 0,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": True,
        "is_paged": False,
    },
    Optimizer.RMSPROP: {
        "alpha": 0.99,
        "eps": 1e-8,
        "weight_decay": 0,
        "momentum": 0,
        "centered": False,
        "optim_bits": 32,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": True,
    },
    Optimizer.RMSPROP_8BIT: {
        "alpha": 0.99,
        "eps": 1e-8,
        "weight_decay": 0,
        "momentum": 0,
        "centered": False,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": True,
    },
    Optimizer.SGD_8BIT: {
        "momentum": 0,
        "dampening": 0,
        "weight_decay": 0,
        "nesterov": False,
        "min_8bit_size": 4096,
        "percentile_clipping": 100,
        "block_wise": True,
    },
    Optimizer.SCHEDULE_FREE_ADAMW: {
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-8,
        "weight_decay": 1e-2,
        "r": 0.0,
        "weight_lr_power": 2.0,
        "foreach": False,
    },
    Optimizer.SCHEDULE_FREE_SGD: {
        "momentum": 0,
        "weight_decay": 1e-2,
        "r": 0.0,
        "weight_lr_power": 2.0,
        "foreach": False,
    },
    Optimizer.PRODIGY: {
        "beta1": 0.9,
        "beta2": 0.999,
        "beta3": None,
        "eps": 1e-8,
        "weight_decay": 0,
        "decouple": True,
        "use_bias_correction": False,
        "safeguard_warmup": False,
        "d0": 1e-6,
        "d_coef": 1.0,
        "growth_rate": float('inf'),
        "fsdp_in_use": False,
        "slice_p": 11,
    },
    Optimizer.PRODIGY_PLUS_SCHEDULE_FREE: {
        "beta1": 0.9,
        "beta2": 0.99,
        "beta3": None,
        "weight_decay": 0.0,
        "weight_decay_by_lr": True,
        "use_bias_correction": False,
        "d0": 1e-6,
        "d_coef": 1.0,
        "prodigy_steps": 0,
        "use_speed": False,
        "eps": 1e-8,
        "split_groups": True,
        "split_groups_mean": False,
        "factored": True,
        "factored_fp32": True,
        "fused_back_pass": False,
        "use_stableadamw": True,
        "use_cautious": False,
        "use_grams": False,
        "use_adopt": False,
        "use_focus": False,
        "d_limiter": True,
        "stochastic_rounding": True,
        "use_schedulefree": True,
        "use_orthograd": False,
    },
    Optimizer.DADAPT_ADA_GRAD: {
        "momentum": 0,
        "log_every": 0,
        "weight_decay": 0.0,
        "eps": 0.0,
        "d0": 1e-6,
        "growth_rate": float('inf'),
    },
    Optimizer.DADAPT_ADAN: {
        "beta1": 0.98,
        "beta2": 0.92,
        "beta3": 0.99,
        "eps": 1e-8,
        "weight_decay": 0.02,
        "no_prox": False,
        "log_every": 0,
        "d0": 1e-6,
        "growth_rate": float('inf'),
    },
    Optimizer.DADAPT_ADAM: {
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-8,
        "weight_decay": 0,
        "log_every": 0,
        "decouple": False,
        "use_bias_correction": False,
        "d0": 1e-6,
        "growth_rate": float('inf'),
        "fsdp_in_use": False,
    },
    Optimizer.DADAPT_SGD: {
        "momentum": 0.0,
        "weight_decay": 0,
        "log_every": 0,
        "d0": 1e-6,
        "growth_rate": float('inf'),
        "fsdp_in_use": False,
    },
    Optimizer.DADAPT_LION: {
        "beta1": 0.9,
        "beta2": 0.999,
        "weight_decay": 0.0,
        "log_every": 0,
        "d0": 1e-6,
        "fsdp_in_use": False,
    },
    Optimizer.ADAM: {
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-8,
        "weight_decay": 0,
        "amsgrad": False,
        "foreach": False,
        "maximize": False,
        "capturable": False,
        "differentiable": False,
        "fused": True,
        "stochastic_rounding": False,
        "fused_back_pass": False,
    },
    Optimizer.ADAMW: {
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-8,
        "weight_decay": 1e-2,
        "amsgrad": False,
        "foreach": False,
        "maximize": False,
        "capturable": False,
        "differentiable": False,
        "fused": True,
        "stochastic_rounding": False,
        "fused_back_pass": False,
    },
    Optimizer.SGD: {
        "momentum": 0,
        "dampening": 0,
        "weight_decay": 0,
        "nesterov": False,
        "foreach": False,
        "maximize": False,
        "differentiable": False,
    },
    Optimizer.LION: {
        "beta1": 0.9,
        "beta2": 0.99,
        "weight_decay": 0.0,
        "use_triton": False,
    },
    Optimizer.CAME: {
        "beta1": 0.9,
        "beta2": 0.999,
        "beta3": 0.9999,
        "eps": 1e-30,
        "eps2": 1e-16,
        "weight_decay": 1e-2,
        "stochastic_rounding": False,
        "use_cautious": False,
        "fused_back_pass": False,
    },
    Optimizer.CAME_8BIT: {
        "beta1": 0.9,
        "beta2": 0.999,
        "beta3": 0.9999,
        "eps": 1e-30,
        "eps2": 1e-16,
        "weight_decay": 1e-2,
        "stochastic_rounding": False,
        "fused_back_pass": False,
        "min_8bit_size": 16384,
        "quant_block_size": 2048
    },
    Optimizer.ADAMW_ADV: {
        "beta1": 0.9,
        "beta2": 0.99,
        "eps": 1e-8,
        "weight_decay": 0.0,
        "use_bias_correction": True,
        "nnmf_factor": False,
        "stochastic_rounding": True,
        "fused_back_pass": False,
        "use_atan2": False,
        "cautious_mask": False,
        "grams_moment": False,
        "orthogonal_gradient": False,
        "use_AdEMAMix": False,
        "beta3_ema": 0.9999,
        "alpha": 5,
    },
    Optimizer.ADOPT_ADV: {
        "beta1": 0.9,
        "beta2": 0.9999,
        "eps": 1e-6,
        "weight_decay": 0.0,
        "nnmf_factor": False,
        "stochastic_rounding": True,
        "fused_back_pass": False,
        "use_atan2": False,
        "cautious_mask": False,
        "grams_moment": False,
        "orthogonal_gradient": False,
        "use_AdEMAMix": False,
        "beta3_ema": 0.9999,
        "alpha": 5,
        "Simplified_AdEMAMix": False,
        "alpha_grad": 100.0,
    },
    Optimizer.PRODIGY_ADV: {
        "beta1": 0.9,
        "beta2": 0.99,
        "beta3": None,
        "eps": 1e-8,
        "weight_decay": 0.0,
        "nnmf_factor": False,
        "stochastic_rounding": True,
        "fused_back_pass": False,
        "d0": 1e-6,
        "d_coef": 1.0,
        "growth_rate": float('inf'),
        "slice_p": 11,
        "prodigy_steps": 0,
        "use_atan2": False,
        "cautious_mask": False,
        "grams_moment": False,
        "orthogonal_gradient": False,
        "use_AdEMAMix": False,
        "beta3_ema": 0.9999,
        "alpha": 5,
        "Simplified_AdEMAMix": False,
        "alpha_grad": 100.0,
    },
    Optimizer.SIMPLIFIED_AdEMAMix: {
        "beta1": 0.99,
        "beta2": 0.99,
        "eps": 1e-8,
        "weight_decay": 0.0,
        "alpha_grad": 100.0,
        "beta1_warmup": None,
        "min_beta1": 0.9,
        "use_bias_correction": True,
        "nnmf_factor": False,
        "stochastic_rounding": True,
        "fused_back_pass": False,
        "orthogonal_gradient": False,
    },
    Optimizer.LION_ADV: {
        "beta1": 0.9,
        "beta2": 0.99,
        "weight_decay": 0.0,
        "clip_threshold": None,
        "nnmf_factor": False,
        "stochastic_rounding": True,
        "fused_back_pass": False,
        "cautious_mask": False,
        "orthogonal_gradient": False,
    },
    Optimizer.LION_PRODIGY_ADV: {
        "beta1": 0.9,
        "beta2": 0.99,
        "beta3": None,
        "weight_decay": 0.0,
        "clip_threshold": None,
        "nnmf_factor": False,
        "stochastic_rounding": True,
        "fused_back_pass": False,
        "d0": 1e-6,
        "d_coef": 1.0,
        "growth_rate": float('inf'),
        "slice_p": 11,
        "cautious_mask": False,
        "orthogonal_gradient": False,
    },
    Optimizer.ADABELIEF: {
        "beta1": 0.9,
        "beta2": 0.999,
        "eps": 1e-16,
        "weight_decay": 0,
        "amsgrad": False,
        "decoupled_decay": True,
        "fixed_decay": False,
        "rectify": True,
        "degenerated_to_sgd": True,
    },
    Optimizer.TIGER: {
        "beta1": 0.965,
        "weight_decay": 0.01,
        "decoupled_decay": True,
        "fixed_decay": False,
    },
    Optimizer.AIDA: {
        "beta1": 0.9,
        "beta2": 0.999,
        "k": 2,
        "xi": 1e-20,
        "weight_decay": 0.0,
        "decoupled_decay": False,
        "fixed_decay": False,
        "rectify": False,
        "n_sma_threshold": 5,
        "degenerated_to_sgd": True,
        "ams_bound": False,
        "r": 0.95,
        "adanorm": False,
        "adam_debias": False,
        "eps": 1e-8,
    },
    Optimizer.YOGI: {
        "beta1": 0.9,
        "beta2": 0.999,
        "weight_decay": 0.0,
        "decoupled_decay": True,
        "fixed_decay": False,
        "r": 0.95,
        "adanorm": False,
        "adam_debias": False,
        "initial_accumulator": 1e-6,
        "eps": 1e-3,
    },
}




class OptimizerController(BaseController):
    # @formatter:off
    optimizer_params = {
        "adam_w_mode": {"title": QCA.translate("optimizer_parameter", "Adam W Mode"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use weight decay correction for Adam optimizer."), "type": "bool"},
        "alpha": {"title": QCA.translate("optimizer_parameter", "Alpha"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Smoothing parameter for RMSprop and others."), "type": "float"},
        "amsgrad": {"title": QCA.translate("optimizer_parameter", "AMSGrad"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use the AMSGrad variant for Adam."), "type": "bool"},
        "beta1": {"title": QCA.translate("optimizer_parameter", "Beta1"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "optimizer_momentum term."), "type": "float"},
        "beta2": {"title": QCA.translate("optimizer_parameter", "Beta2"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Coefficients for computing running averages of gradient."), "type": "float"},
        "beta3": {"title": QCA.translate("optimizer_parameter", "Beta3"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Coefficient for computing the Prodigy stepsize."), "type": "float"},
        "bias_correction": {"title": QCA.translate("optimizer_parameter", "Bias Correction"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use bias correction in optimization algorithms like Adam."), "type": "bool"},
        "block_wise": {"title": QCA.translate("optimizer_parameter", "Block Wise"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to perform block-wise model update."), "type": "bool"},
        "capturable": {"title": QCA.translate("optimizer_parameter", "Capturable"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether some property of the optimizer can be captured."), "type": "bool"},
        "centered": {"title": QCA.translate("optimizer_parameter", "Centered"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to center the gradient before scaling. Great for stabilizing the training process."), "type": "bool"},
        "clip_threshold": {"title": QCA.translate("optimizer_parameter", "Clip Threshold"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Clipping value for gradients."), "type": "float"},
        "d0": {"title": QCA.translate("optimizer_parameter", "Initial D"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Initial D estimate for D-adaptation."), "type": "float"},
        "d_coef": {"title": QCA.translate("optimizer_parameter", "D Coefficient"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Coefficient in the expression for the estimate of d."), "type": "float"},
        "dampening": {"title": QCA.translate("optimizer_parameter", "Dampening"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Dampening for optimizer_momentum."), "type": "float"},
        "decay_rate": {"title": QCA.translate("optimizer_parameter", "Decay Rate"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Rate of decay for moment estimation."), "type": "float"},
        "decouple": {"title": QCA.translate("optimizer_parameter", "Decouple"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use AdamW style optimizer_decoupled weight decay."), "type": "bool"},
        "differentiable": {"title": QCA.translate("optimizer_parameter", "Differentiable"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether the optimization function is optimizer_differentiable."), "type": "bool"},
        "eps": {"title": QCA.translate("optimizer_parameter", "EPS"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "A small value to prevent division by zero."), "type": "float"},
        "eps2": {"title": QCA.translate("optimizer_parameter", "EPS 2"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "A small value to prevent division by zero."), "type": "float"},
        "foreach": {"title": QCA.translate("optimizer_parameter", "ForEach"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use a foreach implementation if available. This implementation is usually faster."), "type": "bool"},
        "fsdp_in_use": {"title": QCA.translate("optimizer_parameter", "FSDP in Use"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Flag for using sharded parameters."), "type": "bool"},
        "fused": {"title": QCA.translate("optimizer_parameter", "Fused"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use a fused implementation if available. This implementation is usually faster and requires less memory."), "type": "bool"},
        "fused_back_pass": {"title": QCA.translate("optimizer_parameter", "Fused Back Pass"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to fuse the back propagation pass with the optimizer step. This reduces VRAM usage, but is not compatible with gradient accumulation."), "type": "bool"},
        "growth_rate": {"title": QCA.translate("optimizer_parameter", "Growth Rate"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Limit for D estimate growth rate."), "type": "float"},
        "initial_accumulator_value": {"title": QCA.translate("optimizer_parameter", "Initial Accumulator Value"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Initial value for Adagrad optimizer."), "type": "float"},
        "initial_accumulator": {"title": QCA.translate("optimizer_parameter", "Initial Accumulator"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Sets the starting value for both moment estimates to ensure numerical stability and balanced adaptive updates early in training."), "type": "float"},
        "is_paged": {"title": QCA.translate("optimizer_parameter", "Is Paged"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether the optimizer's internal state should be paged to CPU."), "type": "bool"},
        "log_every": {"title": QCA.translate("optimizer_parameter", "Log Every"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Intervals at which logging should occur."), "type": "int"},
        "lr_decay": {"title": QCA.translate("optimizer_parameter", "LR Decay"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Rate at which learning rate decreases."), "type": "float"},
        "max_unorm": {"title": QCA.translate("optimizer_parameter", "Max Unorm"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Maximum value for gradient clipping by norms."), "type": "float"},
        "maximize": {"title": QCA.translate("optimizer_parameter", "Maximize"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to optimizer_maximize the optimization function."), "type": "bool"},
        "min_8bit_size": {"title": QCA.translate("optimizer_parameter", "Min 8bit Size"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Minimum tensor size for 8-bit quantization."), "type": "int"},
        "quant_block_size": {"title": QCA.translate("optimizer_parameter", "Quant Block Size"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Size of a block of normalized 8-bit quantization data. Larger values increase memory efficiency at the cost of data precision."), "type": "int"},
        "momentum": {"title": QCA.translate("optimizer_parameter", "optimizer_momentum"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Factor to accelerate SGD in relevant direction."), "type": "float"},
        "nesterov": {"title": QCA.translate("optimizer_parameter", "Nesterov"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to enable Nesterov optimizer_momentum."), "type": "bool"},
        "no_prox": {"title": QCA.translate("optimizer_parameter", "No Prox"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use proximity updates or not."), "type": "bool"},
        "optim_bits": {"title": QCA.translate("optimizer_parameter", "Optim Bits"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Number of bits used for optimization."), "type": "int"},
        "percentile_clipping": {"title": QCA.translate("optimizer_parameter", "Percentile Clipping"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Gradient clipping based on percentile values."), "type": "int"},
        "relative_step": {"title": QCA.translate("optimizer_parameter", "Relative Step"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use a relative step size."), "type": "bool"},
        "safeguard_warmup": {"title": QCA.translate("optimizer_parameter", "Safeguard Warmup"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Avoid issues during warm-up stage."), "type": "bool"},
        "scale_parameter": {"title": QCA.translate("optimizer_parameter", "Scale Parameter"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to scale the parameter or not."), "type": "bool"},
        "stochastic_rounding": {"title": QCA.translate("optimizer_parameter", "Stochastic Rounding"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Stochastic rounding for weight updates. Improves quality when using bfloat16 weights."), "type": "bool"},
        "use_bias_correction": {"title": QCA.translate("optimizer_parameter", "Bias Correction"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Turn on Adam's bias correction."), "type": "bool"},
        "use_triton": {"title": QCA.translate("optimizer_parameter", "Use Triton"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether Triton optimization should be used."), "type": "bool"},
        "warmup_init": {"title": QCA.translate("optimizer_parameter", "Warmup Initialization"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to warm-up the optimizer initialization."), "type": "bool"},
        "weight_decay": {"title": QCA.translate("optimizer_parameter", "Weight Decay"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Regularization to prevent overfitting."), "type": "float"},
        "weight_lr_power": {"title": QCA.translate("optimizer_parameter", "Weight LR Power"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "During warmup, the weights in the average will be equal to lr raised to this power. Set to 0 for no weighting."), "type": "float"},
        "decoupled_decay": {"title": QCA.translate("optimizer_parameter", "Decoupled Decay"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "If set as True, then the optimizer uses decoupled weight decay as in AdamW."), "type": "bool"},
        "fixed_decay": {"title": QCA.translate("optimizer_parameter", "Fixed Decay"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "(When Decoupled Decay is True:) Applies fixed weight decay when True; scales decay with learning rate when False."), "type": "bool"},
        "rectify": {"title": QCA.translate("optimizer_parameter", "Rectify"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Perform the rectified update similar to RAdam."), "type": "bool"},
        "degenerated_to_sgd": {"title": QCA.translate("optimizer_parameter", "Degenerated to SGD"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Performs SGD update when gradient variance is high."), "type": "bool"},
        "k": {"title": QCA.translate("optimizer_parameter", "K"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Number of vector projected per iteration."), "type": "int"},
        "xi": {"title": QCA.translate("optimizer_parameter", "Xi"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Term used in vector projections to avoid division by zero."), "type": "float"},
        "n_sma_threshold": {"title": QCA.translate("optimizer_parameter", "N SMA Threshold"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Number of SMA threshold."), "type": "int"},
        "ams_bound": {"title": QCA.translate("optimizer_parameter", "AMS Bound"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use the AMSBound variant."), "type": "bool"},
        "r": {"title": QCA.translate("optimizer_parameter", "R"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "EMA factor."), "type": "float"},
        "adanorm": {"title": QCA.translate("optimizer_parameter", "AdaNorm"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use the AdaNorm variant"), "type": "bool"},
        "adam_debias": {"title": QCA.translate("optimizer_parameter", "Adam Debias"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Only correct the denominator to avoid inflating step sizes early in training."), "type": "bool"},
        "slice_p": {"title": QCA.translate("optimizer_parameter", "Slice parameters"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Reduce memory usage by calculating LR adaptation statistics on only every pth entry of each tensor. For values greater than 1 this is an approximation to standard Prodigy. Values ~11 are reasonable."), "type": "int"},
        "cautious": {"title": QCA.translate("optimizer_parameter", "Cautious"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Whether to use the Cautious variant"), "type": "bool"},
        "weight_decay_by_lr": {"title": QCA.translate("optimizer_parameter", "weight_decay_by_lr"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Automatically adjust weight decay based on lr"), "type": "bool"},
        "prodigy_steps": {"title": QCA.translate("optimizer_parameter", "prodigy_steps"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Turn off Prodigy after N steps"), "type": "int"},
        "use_speed": {"title": QCA.translate("optimizer_parameter", "use_speed"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "use_speed method"), "type": "bool"},
        "split_groups": {"title": QCA.translate("optimizer_parameter", "split_groups"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use split groups when training multiple params(uNet,TE..)"), "type": "bool"},
        "split_groups_mean": {"title": QCA.translate("optimizer_parameter", "split_groups_mean"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use mean for split groups"), "type": "bool"},
        "factored": {"title": QCA.translate("optimizer_parameter", "factored"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use factored"), "type": "bool"},
        "factored_fp32": {"title": QCA.translate("optimizer_parameter", "factored_fp32"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use factored_fp32"), "type": "bool"},
        "use_stableadamw": {"title": QCA.translate("optimizer_parameter", "use_stableadamw"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use use_stableadamw for gradient scaling"), "type": "bool"},
        "use_cautious": {"title": QCA.translate("optimizer_parameter", "use_cautious"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use cautious method"), "type": "bool"},
        "use_grams": {"title": QCA.translate("optimizer_parameter", "use_grams"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use grams method"), "type": "bool"},
        "use_adopt": {"title": QCA.translate("optimizer_parameter", "use_adopt"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use adopt method"), "type": "bool"},
        "use_focus": {"title": QCA.translate("optimizer_parameter", "use_focus"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use focus method"), "type": "bool"},
        "d_limiter": {"title": QCA.translate("optimizer_parameter", "d_limiter"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Prevent over-estimated LRs when gradients and EMA are still stabilizing"), "type": "bool"},
        "use_schedulefree": {"title": QCA.translate("optimizer_parameter", "use_schedulefree"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use Schedulefree method"), "type": "bool"},
        "use_orthograd": {"title": QCA.translate("optimizer_parameter", "use_orthograd"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Use orthograd method"), "type": "bool"},
        "nnmf_factor": {"title": QCA.translate("optimizer_parameter", "Factored Optimizer"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Enables a memory-efficient mode by applying fast low-rank factorization to the optimizers states. It combines factorization for magnitudes with 1-bit compression for signs, drastically reducing VRAM usage and allowing for larger models or batch sizes. This is an approximation which may slightly alter training dynamics."), "type": "bool"},
        "orthogonal_gradient": {"title": QCA.translate("optimizer_parameter", "OrthoGrad"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Reduces overfitting by removing the gradient component parallel to the weight, thus improving generalization."), "type": "bool"},
        "use_atan2": {"title": QCA.translate("optimizer_parameter", "Atan2 Scaling"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "A robust replacement for eps, which also incorporates gradient clipping, bounding and stabilizing the optimizer updates."), "type": "bool"},
        "cautious_mask": {"title": QCA.translate("optimizer_parameter", "Cautious Variant"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Applies a mask to dampen or zero-out momentum components that disagree with the current gradients direction."), "type": "bool"},
        "grams_moment": {"title": QCA.translate("optimizer_parameter", "GRAMS Variant"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Aligns the momentum direction with the current gradient direction while preserving its accumulated magnitude."), "type": "bool"},
        "use_AdEMAMix": {"title": QCA.translate("optimizer_parameter", "AdEMAMix EMA"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Adds a second, slow-moving EMA, which is combined with the primary momentum to stabilize updates, and accelerate the training."), "type": "bool"},
        "beta3_ema": {"title": QCA.translate("optimizer_parameter", "Beta3 EMA"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Coefficient for slow-moving EMA of AdEMAMix."), "type": "float"},
        "beta1_warmup": {"title": QCA.translate("optimizer_parameter", "Beta1 Warmup Steps"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Number of warmup steps to gradually increase beta1 from Minimum Beta1 Value to its final value. During warmup, beta1 increases linearly. leave it empty to disable warmup and use constant beta1."), "type": "int"},
        "min_beta1": {"title": QCA.translate("optimizer_parameter", "Minimum Beta1"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Starting beta1 value for warmup scheduling. Used only when beta1 warmup is enabled. Lower values allow faster initial adaptation, while higher values provide more smoothing. The final beta1 value is specified in the beta1 parameter."), "type": "float"},
        "Simplified_AdEMAMix": {"title": QCA.translate("optimizer_parameter", "Simplified AdEMAMix"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Enables a simplified, single-EMA variant of AdEMAMix. Instead of blending two moving averages (fast and slow momentum), this version combines the raw current gradient (controlled by 'Grad α') directly with a single theory-based momentum. This makes the optimizer highly responsive to recent gradient information, which can accelerate training in all batch size scenarios when tuned correctly."), "type": "bool"},
        "alpha_grad": {"title": QCA.translate("optimizer_parameter", "Grad α"), "tooltip": QCA.translate("optimizer_parameter_tooltip", "Controls the mixing coefficient between raw gradients and momentum gradients in Simplified AdEMAMix. Higher values (e.g., 10-100) emphasize recent gradients, suitable for small batch sizes to reduce noise. Lower values (e.g., 0-1) emphasize historical gradients, suitable for large batch sizes for stability. Setting to 0 uses only momentum gradients without raw gradient contribution."), "type": "float"},
    }

    # Quick way of connecting controls without redefining every single one of them.
    state_ui_connections = {
        "optimizer.{}".format(k): "{}{}".format(k, "Cbx" if v["type"] == "bool" else ("Sbx" if v["type"] == "int" else "Led")) for k, v in optimizer_params.items()
    }

    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/optimizer.ui", state=state, mutex=mutex, name=None, parent=parent)


        callback = self.__updateOptimizer(from_index=False)
        QtW.QApplication.instance().optimizerChanged.connect(callback)
        QtW.QApplication.instance().stateChanged.connect(lambda: callback(self.state.optimizer.optimizer))

    def setup(self):
        row = 0
        for k in sorted(self.optimizer_params.keys()):
            v = self.optimizer_params[k]

            if v["type"] == "bool":
                wdg_name = "{}{}".format(k, "Cbx")
                wdg = QtW.QCheckBox(parent=self.ui, text=v["title"], objectName=wdg_name)
                wdg.setToolTip(v["tooltip"])
                self.ui.optimizerLay.addWidget(wdg, row, 0, 1, 2)
            else:
                wdg_name = "{}{}".format(k, "Lbl")
                lbl = QtW.QLabel(parent=self.ui, text=v["title"], objectName=wdg_name)
                if v["type"] == "int":
                    wdg_name = "{}{}".format(k, "Sbx")
                    wdg = QtW.QSpinBox(parent=self.ui, objectName=wdg_name)
                    wdg.setMinimum(-999999)
                    wdg.setMaximum(999999)
                else:
                    wdg_name = "{}{}".format(k, "Led")
                    wdg = SNLineEdit(parent=self.ui, objectName=wdg_name)
                wdg.setToolTip(v["tooltip"])
                lbl.setBuddy(wdg)
                self.ui.optimizerLay.addWidget(lbl, row, 0, 1, 1)
                self.ui.optimizerLay.addWidget(wdg, row, 1, 1, 1)

            row += 1

    def __updateOptimizer(self, from_index=False):
        def f(idx):
            self.parent.ui.optimizerCmb.blockSignals(True)
            self.parent.ui.optimizerCmb.setCurrentIndex(idx)
            self.parent.ui.optimizerCmb.blockSignals(False)

            self.__updateOptimizerControls(self.ui.optimizerCmb.currentData())


        def g(optimizer):
            self.parent.ui.optimizerCmb.blockSignals(True)
            self.parent.ui.optimizerCmb.setCurrentIndex(self.parent.ui.optimizerCmb.findData(optimizer))
            self.parent.ui.optimizerCmb.blockSignals(False)

            self.__updateOptimizerControls(optimizer)

        return f if from_index else g

    def __updateOptimizerControls(self, optimizer):
        # TODO: setVisible inside a QGridLayout does not rearrange objects. So either create and connect them here, or subclass the layout and make one dynamic.
        # QGridLayout has no direct children, therefore, we must retrieve them in a different way.
        for k, v in self.optimizer_params.items():
            if v["type"] == "bool":
                wdg = self.ui.findChild(QtW.QCheckBox, "{}Cbx".format(k))
                if wdg is not None:
                    wdg.setVisible(k in OPTIMIZER_DEFAULT_PARAMETERS[optimizer])
            else:
                wdg = self.ui.findChild(QtW.QLabel, "{}Lbl".format(k))
                if wdg is not None:
                    wdg.setVisible(k in OPTIMIZER_DEFAULT_PARAMETERS[optimizer])
                if v["type"] == "int":
                    wdg = self.ui.findChild(QtW.QSpinBox, "{}Sbx".format(k))
                else:
                    wdg = self.ui.findChild(SNLineEdit, "{}Led".format(k))
                if wdg is not None:
                    wdg.setVisible(k in OPTIMIZER_DEFAULT_PARAMETERS[optimizer])

    def __loadDefaults(self):
        optimizer = self.ui.optimizerCmb.currentData()
        for k, v in OPTIMIZER_DEFAULT_PARAMETERS[optimizer].items():
            self._setState("optimizer.{}".format(k), v)
        QtW.QApplication.instance().stateChanged.emit()
        QtW.QApplication.instance().optimizerChanged.emit(optimizer)

    def connectUIBehavior(self):
        self.ui.optimizerCmb.activated.connect(self.__updateOptimizer(from_index=True))
        self.ui.loadDefaultsBtn.clicked.connect(lambda: self.__loadDefaults())