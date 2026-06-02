from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = REPO_ROOT / ".env.local"
MODEL_ID = "qwen/qwen3-next-80b-a3b-instruct:free"


def write_env(api_key: str) -> None:
    api_key = sanitize_api_key(api_key)
    content = "\n".join(
        [
            "# Local Oli configuration. Do not commit.",
            'OLI_MODEL_PROVIDER="openai_compatible"',
            'OLI_OPENAI_COMPAT_BASE_URL="https://openrouter.ai/api/v1"',
            f'OLI_OPENAI_COMPAT_MODEL="{MODEL_ID}"',
            f'OLI_OPENAI_COMPAT_API_KEY="{api_key}"',
            "",
        ]
    )
    ENV_PATH.write_text(content, encoding="utf-8")


def sanitize_api_key(api_key: str) -> str:
    value = api_key.strip().strip('"').strip("'")
    lowered = value.lower()
    if lowered.startswith("authorization:"):
        value = value.split(":", 1)[1].strip()
        lowered = value.lower()
    if lowered.startswith("bearer "):
        value = value[7:].strip()
    return value


def main() -> None:
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.title("Configurar OpenRouter para Oli")
    root.geometry("560x220")
    root.resizable(False, False)

    label = tk.Label(
        root,
        text=(
            "Pega tu OpenRouter API key.\n"
            "Se guardara localmente en .env.local y no se subira a Git."
        ),
        justify="left",
        anchor="w",
    )
    label.pack(fill="x", padx=18, pady=(18, 8))

    key_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=key_var, show="*", width=72)
    entry.pack(fill="x", padx=18)
    entry.focus_set()

    model_label = tk.Label(
        root,
        text=f"Modelo: {MODEL_ID}",
        justify="left",
        anchor="w",
        fg="#555555",
    )
    model_label.pack(fill="x", padx=18, pady=(10, 0))

    def save() -> None:
        api_key = sanitize_api_key(key_var.get())
        if not api_key:
            messagebox.showerror("Falta la key", "Pega la API key antes de guardar.")
            return
        write_env(api_key)
        messagebox.showinfo("Listo", f"OpenRouter quedo configurado en:\n{ENV_PATH}")
        root.destroy()

    button = tk.Button(root, text="Guardar configuracion", command=save)
    button.pack(pady=18)

    root.mainloop()


if __name__ == "__main__":
    main()
