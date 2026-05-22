<h2 align="center">DEAL: Data-Efficient Adversarial Learning for High-Quality Infrared Imaging</h2>

Zhu Liu†, Zijun Wang†, Jinyuan Liu‡, Fanqi Meng†, Long Ma†, Risheng Liu†*

†School of Software Technology, Dalian University of Technology  
‡School of Mechanical Engineering, Dalian University of Technology

---

## Attribution & This Repository

**Original algorithm and publication (CVPR 2025)**  
The DEAL method, training code, network design, and experimental claims belong to the authors above. The official implementation is maintained at **[LiuZhu-CV/DEAL](https://github.com/LiuZhu-CV/DEAL)**. Please cite the original paper when using the method in research (see [Citation](#smiley-citation)).

**This repository ([NorthBridgeAthlon64/DEAL](https://github.com/NorthBridgeAthlon64/DEAL))**  
A community fork for local deployment and demonstration. It **does not** replace or represent the authors’ official release. Core model code under `DEAL/` is derived from the upstream project; extensions below are additional engineering work on this fork only:

| Component | Description |
|-----------|-------------|
| `backend/` | Flask API wrapping infrared enhancement (`inference.py`, `app.py`) |
| `frontend/` | Vue 3 + Vite UI for upload, preview, and download |
| `scripts/` | Windows launch scripts for backend and frontend |
| `.gitignore` | Ignore checkpoints, datasets, and runtime upload/result dirs |
| README (Web Demo) | Usage docs for the web stack |

**Acknowledgement**  
We thank the DEAL authors for open-sourcing their work. If you find the method useful, please star the [official repository](https://github.com/LiuZhu-CV/DEAL) and cite the CVPR 2025 paper.

**Disclaimer**  
Pretrained weights and datasets are distributed via the authors’ links (e.g. Baidu Netdisk in the sections below), not bundled in this repo. Use them only in accordance with the original project’s terms and applicable licenses.

---

:star: If DEAL is helpful for you, please star the **official** repo as well. Thanks!

## :book: Table Of Contents

- [Attribution & This Repository](#attribution--this-repository)
- [TODO](#todo)
- [Abstract](#abstract)
- [Framework Overview](#framework_overview)
- [Visual Display](#visual_comparison)
- [Setup](#setup)
- [Training](#training)
- [Test](#inference)
- [Web Demo](#web-demo)

<!-- - [Installation](#installation)

- [Inference](#inference) -->

## <a name="todo"></a>:hourglass: TODO

- [x] Release Code ​1​.​0:computer:
- [ ] Release benchmark ​

## <a name="abstract"></a>:fireworks: Abstract

> Thermal imaging is often compromised by dynamic, complex degradations caused by hardware limitations and unpredictable environmental factors. 
The scarcity of high-quality infrared data, coupled with the challenges of dynamic, intricate degradations, makes it difficult to recover details using existing methods. 
In this paper, we introduce thermal degradation simulation integrated into the training process via a mini-max optimization, by modeling these degraded factors as adversarial attacks on thermal images. 
The simulation is dynamic to maximize objective functions, thus capturing a broad spectrum of degraded data distributions.
 This approach enables training with limited data, thereby improving model performance. Additionally, we introduce a dual-interaction network that combines the benefits
  of spiking neural networks with scale transformation to capture degraded features with sharp spike signal inten- sities. This architecture ensures compact model parameters 
  while preserving eficient feature representation. Extensive experiments demonstrate that our method not only achieves superior visual quality under diverse single and composited degradation, 
  but also delivers a significant reduction in processing when trained on only fifty clear images, outperforming existing techniques in eficiency and accuracy. 

## <a name="framework_overview"></a>:eyes: Framework Overview

![main_00](./assets/main_00.png)

:star: Overview of DEAL. We present a data-efficient adversarial learning strategy, which constructs the dynamic degradation generation to guide the image enhancement procedure with a Dynamic Adversarial Solution (DAS) at (a). The concrete architecture of dual interaction network, consisting of Scale Transform Module (STM) and Spiking-guided Separation Module (SSM) is shown at (b). Spiking-guided Separation to capture sharp intensities of thermal degradations is depicted at (c).

## <a name="visual_comparison"></a>:chart_with_upwards_trend: Visual Display

<img src="./assets/ours.gif" height="421px"> <img src="./assets/ours_output.gif" height="421px">

<img src="./assets/ours_out_depth.gif" height="421px"> <img src="./assets/ours_good.gif" height="421px">

#### Visual display on stripe noise

![stripe_00](./assets/stripe_00.png)

#### Visual display on super-resolution

![SR4_00](./assets/SR4_00.png)

#### Visual display on composited degradation

![混合降秩_00](./assets/混合降秩_00.png)

## <a name="setup"></a> ⚙️ Setup
```bash
conda env create -f environment.yaml
```
#### We will compile as many infrared enhancement-related comparison methods and our experimental results as possible into the following link as soon as possible.

## <a name="training"></a> :wrench: Training

#### Step1: Prepare training data
We train the DEAL on M3FD [[Baidu Netdisk]](https://pan.baidu.com/s/19Q_KuApT30tRP5p14Dyrug?pwd=u49w ) . The final 50 photos used for training are [here](https://pan.baidu.com/s/1da8xgTW3CmVP-RCuAKViJQ?pwd=rd19).

#### Step2: Training for DEAL

cd /DEAL/DEAL1.0/scripts

```bash
python train.py
```

## <a name="inference"></a> 💫 Test

#### Step1: Download the pretrained models

If you want to perform some tests on our model, download the pretrained model [[Baidu Netdisk]](https://pan.baidu.com/s/1XW1zbj0FKdUTefi7fjiXKg?pwd=kiuy) 

#### Step3: Inference for DEAL

run:

```bash
cd DEAL
python LoadOurs.py
```

## <a name="web-demo"></a> Web Demo

Browser-based infrared enhancement (Vue 3 + Flask), aligned with [TarDAL-Poss](https://github.com/JinyuanLiu-CV/TarDAL) layout.

### Prerequisites

1. Conda environment with PyTorch + CUDA (e.g. `conda activate TarDAL`)
2. Pretrained weights at `DEAL/checkpoint/epoch_839_res_model.pt` ([Baidu Netdisk](https://pan.baidu.com/s/1XW1zbj0FKdUTefi7fjiXKg?pwd=kiuy))
3. Node.js 18+ for the frontend

### Start (development)

**Terminal 1 — backend**

```bash
scripts/start-backend.bat
# or: cd backend && python app.py
```

**Terminal 2 — frontend**

```bash
scripts/start-frontend.bat
# or: cd frontend && npm install && npm run dev
```

Open: `http://127.0.0.1:5173/DEAL/`

### API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/upload` | Form field `ir_image` |
| POST | `/api/process` | JSON `{ "session_id": "..." }` |
| GET | `/api/result/<filename>` | Enhanced PNG |
| DELETE | `/api/cleanup/<session_id>` | Remove session files |

### Production (single port)

```bash
cd frontend && npm run build
set DEAL_SERVE_FRONTEND=1
cd ../backend && python app.py
```

Visit: `http://127.0.0.1:5000/DEAL/`

## :smiley: Citation

Please cite the **original DEAL paper** if the method is useful for your research:

```
@inproceedings{liu2025deal,
  title={DEAL: Data-Efficient Adversarial Learning for High-Quality Infrared Imaging},
  author={Liu, Zhu and Wang, Zijun and Liu, Jinyuan and Meng, Fanqi and Ma, Long and Liu, Risheng},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  year={2025}
}
```

The web demo layer in this fork is optional tooling; it is **not** part of the published method and should not be cited as DEAL itself.

## :envelope: Contact

**Original authors (algorithm & paper):** liuzhu@mail.dlut.edu.cn, wzijun6@gmail.com, mengfq0525@gmail.com  

**This fork (web demo / deployment issues):** open an [Issue](https://github.com/NorthBridgeAthlon64/DEAL/issues) on this repository.

