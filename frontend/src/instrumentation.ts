export async function register() {
  if (
    typeof localStorage !== "undefined" &&
    typeof localStorage.getItem !== "function"
  ) {
    const store: Record<string, string> = {};
    (global as unknown as Record<string, unknown>).localStorage = {
      getItem: (k: string) => store[k] ?? null,
      setItem: (k: string, v: string) => { store[k] = v; },
      removeItem: (k: string) => { delete store[k]; },
      clear: () => { Object.keys(store).forEach((k) => delete store[k]); },
      get length() { return Object.keys(store).length; },
      key: (i: number) => Object.keys(store)[i] ?? null,
    };
  }
}
