"""DEAL infrared enhancement inference wrapper for Flask API."""

from __future__ import annotations

import os
import sys
import warnings
from pathlib import Path

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from PIL import Image

warnings.filterwarnings(
    "ignore",
    message="Default upsampling behavior when mode=bilinear is changed to align_corners=False",
)
warnings.filterwarnings("ignore", category=UserWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEAL_ROOT = PROJECT_ROOT / "DEAL"
if str(DEAL_ROOT) not in sys.path:
    sys.path.insert(0, str(DEAL_ROOT))

from models.snn import cleaner as CleanerNet  # noqa: E402

_transform = transforms.Compose([transforms.ToTensor()])

_model: nn.Module | None = None
_device: torch.device | None = None


def _process_max_side() -> int:
    raw = os.environ.get("PROCESS_MAX_SIDE", "1024").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 1024


def _default_ckpt() -> Path:
    env = os.environ.get("DEAL_CKPT", "").strip()
    if env:
        return Path(env)
    return DEAL_ROOT / "checkpoint" / "epoch_839_res_model.pt"


def _resolve_device() -> torch.device:
    spec = os.environ.get("DEAL_DEVICE", "cuda:0").strip()
    if spec.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available but DEAL_DEVICE requests GPU.")
    return torch.device(spec)


def init_model() -> bool:
    """Load DEAL cleaner once at server startup."""
    global _model, _device
    if _model is not None:
        return True

    ckpt = _default_ckpt()
    if not ckpt.is_file():
        raise FileNotFoundError(f"Checkpoint not found: {ckpt}")

    _device = _resolve_device()
    net = CleanerNet().to(_device)
    if _device.type == "cuda":
        device_ids = [int(str(_device).split(":")[-1])] if ":" in str(_device) else [0]
        net = nn.DataParallel(net, device_ids=device_ids)

    state = torch.load(str(ckpt), map_location=_device, weights_only=False)
    net.load_state_dict(state)
    net.eval()
    _model = net
    return True


def is_model_loaded() -> bool:
    return _model is not None


def _load_and_tensor(ir_path: Path) -> torch.Tensor:
    max_side = _process_max_side()
    img = Image.open(ir_path).convert("RGB")
    if max_side > 0:
        w, h = img.size
        long_side = max(w, h)
        if long_side > max_side:
            scale = max_side / long_side
            img = img.resize((int(w * scale), int(h * scale)), Image.BILINEAR)

    x = _transform(img).unsqueeze(0)
    if _device is None:
        raise RuntimeError("Model not initialized.")
    x = x.to(_device)
    if x.shape[1] == 1:
        x = x.expand(1, 3, -1, -1)
    elif x.shape[1] != 3:
        raise ValueError(f"Unexpected channel count: {x.shape[1]}")
    return x


def enhance(ir_path: Path, out_path: Path) -> None:
    """Run single-image infrared enhancement and save result."""
    if _model is None:
        init_model()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with torch.no_grad():
        x = _load_and_tensor(ir_path)
        y = _model(x).squeeze(0)
        torchvision.utils.save_image(y, str(out_path), nrow=1)
