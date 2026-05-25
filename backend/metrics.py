"""Input vs output comparison metrics for infrared enhancement demo."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEAL_ROOT = PROJECT_ROOT / "DEAL"
if str(DEAL_ROOT) not in sys.path:
    sys.path.insert(0, str(DEAL_ROOT))

from models.utilities import ssim as deal_ssim  # noqa: E402

_transform = transforms.Compose([transforms.ToTensor()])


def _process_max_side() -> int:
    raw = os.environ.get("PROCESS_MAX_SIDE", "1024").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 1024


def load_image_tensor(path: Path) -> torch.Tensor:
    """Load image to [1, 3, H, W] in [0, 1], matching inference preprocessing."""
    max_side = _process_max_side()
    img = Image.open(path).convert("RGB")
    if max_side > 0:
        w, h = img.size
        long_side = max(w, h)
        if long_side > max_side:
            scale = max_side / long_side
            img = img.resize((int(w * scale), int(h * scale)), Image.BILINEAR)

    tensor = _transform(img).unsqueeze(0)
    if tensor.shape[1] == 1:
        tensor = tensor.expand(1, 3, -1, -1)
    return tensor


def _to_gray(tensor: torch.Tensor) -> torch.Tensor:
    if tensor.shape[1] == 1:
        return tensor
    return (
        0.299 * tensor[:, 0:1]
        + 0.587 * tensor[:, 1:2]
        + 0.114 * tensor[:, 2:3]
    )


def psnr(ref: torch.Tensor, test: torch.Tensor) -> float:
    mse = torch.mean((ref - test) ** 2)
    if mse.item() <= 1e-12:
        return 100.0
    return float(20 * torch.log10(1.0 / torch.sqrt(mse)).item())


def ssim_value(ref: torch.Tensor, test: torch.Tensor) -> float:
    return float(deal_ssim(ref, test).item())


def entropy(tensor: torch.Tensor) -> float:
    gray = _to_gray(tensor).detach().cpu().clamp(0, 1)
    hist = torch.histc(gray, bins=256, min=0.0, max=1.0)
    prob = hist / hist.sum()
    prob = prob[prob > 0]
    return float((-prob * torch.log2(prob)).sum().item())


def gradient_energy(tensor: torch.Tensor) -> float:
    gray = _to_gray(tensor)
    sobel_x = torch.tensor(
        [[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]], dtype=gray.dtype, device=gray.device
    ).unsqueeze(0)
    sobel_y = torch.tensor(
        [[[-1, -2, -1], [0, 0, 0], [1, 2, 1]]], dtype=gray.dtype, device=gray.device
    ).unsqueeze(0)
    gx = F.conv2d(gray, sobel_x, padding=1)
    gy = F.conv2d(gray, sobel_y, padding=1)
    return float(torch.sqrt(gx * gx + gy * gy).mean().item())


def _relative_gain(before: float, after: float) -> float:
    if abs(before) < 1e-8:
        return 0.0
    return (after - before) / before * 100.0


def improvement_pct(input_tensor: torch.Tensor, output_tensor: torch.Tensor) -> float:
    entropy_gain = _relative_gain(entropy(input_tensor), entropy(output_tensor))
    gradient_gain = _relative_gain(
        gradient_energy(input_tensor), gradient_energy(output_tensor)
    )
    return 0.7 * entropy_gain + 0.3 * gradient_gain


def evaluate_pair(input_path: Path, output_path: Path, elapsed_sec: float) -> dict:
    input_tensor = load_image_tensor(input_path)
    output_tensor = load_image_tensor(output_path)

    return {
        "psnr": round(psnr(input_tensor, output_tensor), 2),
        "ssim": round(ssim_value(input_tensor, output_tensor), 3),
        "improvement": round(improvement_pct(input_tensor, output_tensor), 1),
        "time": round(elapsed_sec, 2),
    }
