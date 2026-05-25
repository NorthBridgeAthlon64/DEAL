function toGray(r, g, b) {
  return 0.299 * r + 0.587 * g + 0.114 * b;
}

function imageDataToGray(imageData) {
  const { data, width, height } = imageData;
  const gray = new Float32Array(width * height);
  for (let i = 0, p = 0; i < data.length; i += 4, p += 1) {
    gray[p] = toGray(data[i], data[i + 1], data[i + 2]) / 255;
  }
  return { gray, width, height };
}

function psnrFromGray(a, b) {
  let mse = 0;
  for (let i = 0; i < a.length; i += 1) {
    const diff = a[i] - b[i];
    mse += diff * diff;
  }
  mse /= a.length;
  if (mse <= 1e-12) return 100;
  return 20 * Math.log10(1 / Math.sqrt(mse));
}

function ssimFromGray(a, b, width, height) {
  const size = a.length;
  let meanA = 0;
  let meanB = 0;
  for (let i = 0; i < size; i += 1) {
    meanA += a[i];
    meanB += b[i];
  }
  meanA /= size;
  meanB /= size;

  let varA = 0;
  let varB = 0;
  let cov = 0;
  for (let i = 0; i < size; i += 1) {
    const da = a[i] - meanA;
    const db = b[i] - meanB;
    varA += da * da;
    varB += db * db;
    cov += da * db;
  }
  varA /= size - 1;
  varB /= size - 1;
  cov /= size - 1;

  const c1 = 0.01 ** 2;
  const c2 = 0.03 ** 2;
  const numerator = (2 * meanA * meanB + c1) * (2 * cov + c2);
  const denominator = (meanA * meanA + meanB * meanB + c1) * (varA + varB + c2);
  return denominator === 0 ? 1 : numerator / denominator;
}

function entropyFromGray(gray) {
  const hist = new Array(256).fill(0);
  for (let i = 0; i < gray.length; i += 1) {
    const bin = Math.min(255, Math.max(0, Math.floor(gray[i] * 255)));
    hist[bin] += 1;
  }
  let entropy = 0;
  for (let i = 0; i < 256; i += 1) {
    if (hist[i] === 0) continue;
    const p = hist[i] / gray.length;
    entropy -= p * Math.log2(p);
  }
  return entropy;
}

function gradientEnergyFromGray(gray, width, height) {
  let sum = 0;
  let count = 0;
  for (let y = 1; y < height - 1; y += 1) {
    for (let x = 1; x < width - 1; x += 1) {
      const idx = y * width + x;
      const gx =
        -gray[idx - width - 1] -
        2 * gray[idx - 1] -
        gray[idx + width - 1] +
        gray[idx - width + 1] +
        2 * gray[idx + 1] +
        gray[idx + width + 1];
      const gy =
        -gray[idx - width - 1] -
        2 * gray[idx - width] -
        gray[idx - width + 1] +
        gray[idx + width - 1] +
        2 * gray[idx + width] +
        gray[idx + width + 1];
      sum += Math.sqrt(gx * gx + gy * gy);
      count += 1;
    }
  }
  return count ? sum / count : 0;
}

function relativeGain(before, after) {
  if (Math.abs(before) < 1e-8) return 0;
  return ((after - before) / before) * 100;
}

export function evaluateImageDataPair(inputData, outputData, elapsedSec = 0) {
  const inputGray = imageDataToGray(inputData);
  const outputGray = imageDataToGray(outputData);

  const entropyIn = entropyFromGray(inputGray.gray);
  const entropyOut = entropyFromGray(outputGray.gray);
  const gradientIn = gradientEnergyFromGray(
    inputGray.gray,
    inputGray.width,
    inputGray.height,
  );
  const gradientOut = gradientEnergyFromGray(
    outputGray.gray,
    outputGray.width,
    outputGray.height,
  );

  const improvement =
    0.7 * relativeGain(entropyIn, entropyOut) +
    0.3 * relativeGain(gradientIn, gradientOut);

  return {
    psnr: psnrFromGray(inputGray.gray, outputGray.gray),
    ssim: ssimFromGray(
      inputGray.gray,
      outputGray.gray,
      inputGray.width,
      inputGray.height,
    ),
    improvement,
    time: elapsedSec,
  };
}

export function formatBackendMetrics(raw = {}) {
  return {
    psnr: raw.psnr != null ? Number(raw.psnr).toFixed(2) : '—',
    ssim: raw.ssim != null ? Number(raw.ssim).toFixed(3) : '—',
    improvement:
      raw.improvement != null ? `${Number(raw.improvement).toFixed(1)}%` : '—',
    time: raw.time != null ? `${Number(raw.time).toFixed(2)}s` : '—',
  };
}
