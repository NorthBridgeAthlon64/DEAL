<template>
  <section class="enhancer-shell">
    <div
      class="upload-area"
      :class="{ dragover: dragOver, 'has-image': !!previewUrl }"
      @click="triggerFile"
      @dragover.prevent="dragOver = true"
      @dragleave.prevent="dragOver = false"
      @drop.prevent="onDrop"
    >
      <template v-if="!previewUrl">
        <div class="upload-icon">IR</div>
        <div class="upload-text">上传红外图像</div>
        <div class="upload-hint">点击或拖拽 PNG / JPG / BMP 到此处</div>
      </template>
      <img v-else class="upload-preview" :src="previewUrl" alt="红外预览" />
      <input
        ref="fileInput"
        type="file"
        accept="image/png,image/jpeg,image/bmp,image/jpg"
        class="hidden"
        @change="onFileChange"
      />
    </div>

    <div class="control-panel">
      <button class="btn primary" :disabled="!selectedFile || processing" @click="runEnhance">
        {{ processing ? '增强处理中...' : '开始增强' }}
      </button>
      <button class="btn secondary" :disabled="processing" @click="clearAll">
        清空重置
      </button>
      <button class="btn secondary" :disabled="!resultUrl || processing" @click="downloadResult">
        下载结果
      </button>
      <span class="status-text">{{ statusText }}</span>
    </div>

    <div v-if="processing" class="progress-bar">
      <div class="progress" :style="{ width: `${progress}%` }"></div>
    </div>

    <p v-if="errorMessage" class="msg error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="msg success">{{ successMessage }}</p>

    <div v-if="previewUrl || resultUrl" class="result-section">
      <h3>对比结果</h3>
      <div class="compare-row">
        <div class="compare-card">
          <h4>原始红外</h4>
          <img v-if="previewUrl" :src="previewUrl" alt="原始" />
          <div v-else class="placeholder">暂无</div>
        </div>
        <div class="compare-card">
          <h4>增强结果</h4>
          <img v-if="resultUrl" :src="resultUrl" alt="增强结果" />
          <div v-else class="placeholder">{{ processing ? '处理中...' : '等待增强' }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onBeforeUnmount, ref } from 'vue';

const API_BASE = import.meta.env.VITE_API_BASE ?? '';

const fileInput = ref(null);
const selectedFile = ref(null);
const previewUrl = ref('');
const resultUrl = ref('');
const sessionId = ref('');
const resultFilename = ref('');
const processing = ref(false);
const dragOver = ref(false);
const progress = ref(0);
const errorMessage = ref('');
const successMessage = ref('');
const statusText = ref('请上传一张红外图像');

function revokePreview() {
  if (previewUrl.value && previewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(previewUrl.value);
  }
}

function setPreview(file) {
  revokePreview();
  selectedFile.value = file;
  previewUrl.value = URL.createObjectURL(file);
  resultUrl.value = '';
  resultFilename.value = '';
  sessionId.value = '';
  errorMessage.value = '';
  successMessage.value = '';
  statusText.value = `已选择: ${file.name}`;
}

function triggerFile() {
  fileInput.value?.click();
}

function onFileChange(event) {
  const file = event.target.files?.[0];
  if (file) setPreview(file);
  event.target.value = '';
}

function onDrop(event) {
  dragOver.value = false;
  const file = event.dataTransfer.files?.[0];
  if (file && file.type.startsWith('image/')) setPreview(file);
}

async function cleanupSession() {
  if (!sessionId.value) return;
  try {
    await fetch(`${API_BASE}/api/cleanup/${sessionId.value}`, { method: 'DELETE' });
  } catch {
    /* ignore */
  }
}

async function clearAll() {
  await cleanupSession();
  revokePreview();
  if (resultUrl.value && resultUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(resultUrl.value);
  }
  selectedFile.value = null;
  previewUrl.value = '';
  resultUrl.value = '';
  sessionId.value = '';
  resultFilename.value = '';
  processing.value = false;
  progress.value = 0;
  errorMessage.value = '';
  successMessage.value = '';
  statusText.value = '请上传一张红外图像';
}

async function runEnhance() {
  if (!selectedFile.value || processing.value) return;

  processing.value = true;
  progress.value = 10;
  errorMessage.value = '';
  successMessage.value = '';
  statusText.value = '正在上传...';

  try {
    const form = new FormData();
    form.append('ir_image', selectedFile.value);

    const uploadRes = await fetch(`${API_BASE}/api/upload`, {
      method: 'POST',
      body: form,
    });
    const uploadData = await uploadRes.json();
    if (!uploadRes.ok || !uploadData.success) {
      throw new Error(uploadData.error || '上传失败');
    }

    sessionId.value = uploadData.session_id;
    progress.value = 45;
    statusText.value = '正在增强...';

    const processRes = await fetch(`${API_BASE}/api/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId.value }),
    });
    const processData = await processRes.json();
    if (!processRes.ok || !processData.success) {
      throw new Error(processData.error || '增强失败');
    }

    resultFilename.value = processData.result_filename;
    resultUrl.value = `${API_BASE}/api/result/${resultFilename.value}?t=${Date.now()}`;
    progress.value = 100;
    successMessage.value = '红外图像增强完成';
    statusText.value = '处理完成';
  } catch (err) {
    errorMessage.value = err.message || '请求失败，请确认后端已启动';
    statusText.value = '处理失败';
  } finally {
    processing.value = false;
  }
}

function downloadResult() {
  if (!resultUrl.value) return;
  const a = document.createElement('a');
  a.href = resultUrl.value;
  a.download = resultFilename.value || 'enhanced.png';
  a.target = '_blank';
  a.click();
}

onBeforeUnmount(() => {
  revokePreview();
});
</script>

<style scoped>
.enhancer-shell {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(8px);
}

.upload-area {
  border: 2px dashed rgba(148, 163, 184, 0.4);
  border-radius: 12px;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}

.upload-area:hover,
.upload-area.dragover {
  border-color: #38bdf8;
  background: rgba(56, 189, 248, 0.08);
}

.upload-area.has-image {
  padding: 0.5rem;
}

.upload-icon {
  font-size: 2rem;
  font-weight: 800;
  color: #38bdf8;
  letter-spacing: 0.1em;
}

.upload-text {
  margin-top: 0.75rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.upload-hint {
  margin-top: 0.35rem;
  font-size: 0.85rem;
  opacity: 0.65;
}

.upload-preview {
  max-width: 100%;
  max-height: 360px;
  object-fit: contain;
  border-radius: 8px;
}

.control-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
  margin-top: 1.25rem;
}

.btn {
  padding: 0.55rem 1.1rem;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn.primary {
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
  color: #fff;
}

.btn.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.secondary {
  background: rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
  border: 1px solid rgba(148, 163, 184, 0.35);
}

.btn.secondary:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.status-text {
  font-size: 0.85rem;
  opacity: 0.8;
  margin-left: 0.25rem;
}

.progress-bar {
  margin-top: 1rem;
  height: 6px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #0ea5e9, #6366f1);
  transition: width 0.3s ease;
}

.msg {
  margin: 0.75rem 0 0;
  padding: 0.6rem 0.9rem;
  border-radius: 8px;
  font-size: 0.9rem;
}

.msg.error {
  background: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
}

.msg.success {
  background: rgba(34, 197, 94, 0.15);
  color: #86efac;
}

.result-section {
  margin-top: 1.5rem;
}

.result-section h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
}

.compare-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 640px) {
  .compare-row {
    grid-template-columns: 1fr;
  }
}

.compare-card {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 10px;
  padding: 0.75rem;
  text-align: center;
}

.compare-card h4 {
  margin: 0 0 0.5rem;
  font-size: 0.9rem;
  opacity: 0.85;
}

.compare-card img {
  max-width: 100%;
  max-height: 280px;
  object-fit: contain;
  border-radius: 6px;
}

.placeholder {
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.5;
  font-size: 0.9rem;
}
</style>
