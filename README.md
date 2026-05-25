<h2 align="center">DEAL: Data-Efficient Adversarial Learning for High-Quality Infrared Imaging</h2>

Zhu Liu†, Zijun Wang†, Jinyuan Liu‡, Fanqi Meng†, Long Ma†, Risheng Liu†*

†School of Software Technology, Dalian University of Technology  
‡School of Mechanical Engineering, Dalian University of Technology

---

## Attribution & Copyright

**Original authors (CVPR 2025)**  
The DEAL **method**, **paper**, **training/inference code**, **network architecture**, **experimental results**, and **pretrained weights** are the intellectual property of Zhu Liu, Zijun Wang, Jinyuan Liu, Fanqi Meng, Long Ma, Risheng Liu, and their affiliations. The **official** open-source release is:

**[https://github.com/LiuZhu-CV/DEAL](https://github.com/LiuZhu-CV/DEAL)**

When you use the algorithm or report results, please **cite the original CVPR 2025 paper** (see [Citation](#smiley-citation)) and follow the license and usage terms of the upstream repository.

**This fork ([NorthBridgeAthlon64/DEAL](https://github.com/NorthBridgeAthlon64/DEAL))**  
This repository is a **derivative community fork** built **on top of** the authors’ open-source DEAL project. It is intended only for **local deployment and browser demonstration**. It:

- **Does not** represent the official release, authors, or Dalian University of Technology.
- **Does not** modify or replace the scientific claims of the original paper.
- Keeps core model code under `DEAL/` aligned with the upstream implementation; adds optional tooling listed below.

| Added in this fork only | Description |
|-------------------------|-------------|
| `backend/` | Flask API for upload → enhance → download |
| `frontend/` | Vue 3 + Vite web UI (metrics display, in-site paper viewer) |
| `scripts/` | Windows helper scripts to start backend / frontend |
| `.gitignore` | Excludes checkpoints, datasets, `node_modules`, runtime uploads |

**What you must respect when using this fork**

1. **Retain attribution** — Do not remove author names, the upstream link, or citation guidance from this README when redistributing.
2. **Prefer the official repo** for research reproduction, training, and citing the method; use this fork mainly for the Web demo workflow.
3. **Weights & data** — Download pretrained models and datasets only via the authors’ Baidu Netdisk links in [Test](#inference); they are **not** redistributed here.
4. **Web demo is extra tooling** — The Vue/Flask layer is **not** part of the published DEAL method; do not cite the web UI as the paper’s official code.

**Acknowledgement**  
We sincerely thank the DEAL authors for open-sourcing their work. If the method helps your research, please **star and cite the [official repository](https://github.com/LiuZhu-CV/DEAL)**.

---

:star: If DEAL is helpful for you, please star the **official** repo as well. Thanks!

## :book: Table Of Contents

- [Attribution & Copyright](#attribution--copyright)
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

Browser-based infrared enhancement (Vue 3 + Flask). UI layout references [TarDAL-Poss](https://github.com/JinyuanLiu-CV/TarDAL); **model inference still uses the original DEAL code and weights** under `DEAL/`.

### Prerequisites

| Item | Requirement |
|------|-------------|
| Python | Conda env with PyTorch + CUDA (e.g. `conda env create -f environment.yaml` then `conda activate TarDAL`) |
| Weights | Place `epoch_839_res_model.pt` at `DEAL/checkpoint/epoch_839_res_model.pt` ([Baidu Netdisk](https://pan.baidu.com/s/1XW1zbj0FKdUTefi7fjiXKg?pwd=kiuy)) |
| Node.js | 18+ for the frontend (`npm` in `frontend/`) |
| Ports | Backend **5000**, frontend dev server **5173** (both must be free) |

Clone this fork:

```bash
git clone https://github.com/NorthBridgeAthlon64/DEAL.git
cd DEAL
```

### Quick start (two terminals)

You need **both** backend and frontend running. The UI talks to `http://127.0.0.1:5000` for inference.

**Terminal 1 — start backend (Flask + DEAL model)**

Windows (double-click or PowerShell):

```bat
scripts\start-backend.bat
```

Manual:

```powershell
conda activate TarDAL
cd backend
pip install -r requirements.txt
python app.py
```

Linux / macOS:

```bash
conda activate TarDAL
cd backend
pip install -r requirements.txt
python app.py
```

Wait until you see the server listening on port **5000**. Check: [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health) should return OK and `model_loaded: true` after weights are in place.

**Terminal 2 — start frontend (Vite dev server)**

Windows:

```bat
scripts\start-frontend.bat
```

Manual:

```powershell
cd frontend
npm install
npm run dev
```

Linux / macOS:

```bash
cd frontend
npm install
npm run dev
```

**Open in browser**

- Home: [http://127.0.0.1:5173/DEAL/](http://127.0.0.1:5173/DEAL/) or [http://localhost:5173/DEAL/#/](http://localhost:5173/DEAL/#/)
- Go to **个人应用** → upload an infrared image → **开始增强** → view metrics and download the result.

### 快速启动（中文）

1. 从 [官方仓库](https://github.com/LiuZhu-CV/DEAL) 或本 fork 获取代码；**算法版权与引用请以原作者为准**（见上文 [Attribution & Copyright](#attribution--copyright)）。
2. 按 [Setup](#setup) 配置 Conda 环境，并按 [Test](#inference) 下载权重到 `DEAL/checkpoint/epoch_839_res_model.pt`。
3. **终端 1（后端）**：`scripts\start-backend.bat` 或 `cd backend && python app.py`（需先 `conda activate TarDAL`）。
4. **终端 2（前端）**：`scripts\start-frontend.bat` 或 `cd frontend && npm install && npm run dev`。
5. 浏览器打开 `http://127.0.0.1:5173/DEAL/`，在「个人应用」页上传红外图并增强。

### Troubleshooting

| Symptom | What to check |
|---------|----------------|
| Metrics show `—` | Backend not running, or enhancement not finished — start Terminal 1 and click **开始增强** |
| `model_loaded: false` | Missing `DEAL/checkpoint/epoch_839_res_model.pt` |
| Blank page | Use URL with `/DEAL/` base path; hard-refresh after `npm run dev` |
| Port in use | Stop old `python app.py` on 5000 or change `PORT` env var |

### API (backend `:5000`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check + model load status |
| POST | `/api/upload` | Form field `ir_image` |
| POST | `/api/process` | JSON `{ "session_id": "..." }` → returns `metrics` |
| GET | `/api/result/<filename>` | Enhanced PNG |
| DELETE | `/api/cleanup/<session_id>` | Remove session files |

### Production (single port)

Build the frontend, then let Flask serve static files:

```bash
cd frontend && npm run build
```

Windows:

```bat
set DEAL_SERVE_FRONTEND=1
cd ..\backend
python app.py
```

Linux / macOS:

```bash
export DEAL_SERVE_FRONTEND=1
cd ../backend && python app.py
```

Visit: [http://127.0.0.1:5000/DEAL/](http://127.0.0.1:5000/DEAL/)

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

