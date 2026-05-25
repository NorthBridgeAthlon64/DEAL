import { shallowRef } from 'vue';

const STORAGE_KEY = 'deal-theme';
const MEDIA_QUERY = '(prefers-color-scheme: dark)';

function resolveInitialTheme() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === 'light' || stored === 'dark') return stored;
  return window.matchMedia(MEDIA_QUERY).matches ? 'dark' : 'light';
}

function setHtmlTheme(value) {
  document.documentElement.dataset.theme = value;
}

export function useTheme() {
  const theme = shallowRef('light');

  function applyTheme(value) {
    theme.value = value;
    setHtmlTheme(value);
    localStorage.setItem(STORAGE_KEY, value);
  }

  function toggleTheme() {
    applyTheme(theme.value === 'dark' ? 'light' : 'dark');
  }

  if (typeof window !== 'undefined') {
    applyTheme(resolveInitialTheme());
  }

  return {
    theme,
    toggleTheme,
    applyTheme,
  };
}
