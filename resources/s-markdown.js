class SMarkdown extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });

    this.md = window.markdownit({
      html: false,
      linkify: true,
      typographer: true,
    });

    this.container = document.createElement("div");
    this.container.setAttribute("part", "content");
    this.container.className = "markdown";

    const style = document.createElement("style");
    style.textContent = `
      .markdown {
        all: initial;
        font-family: var(--sl-font-sans, sans-serif);
        font-size: var(--sl-font-size-medium, 1rem);
        line-height: 1.6;
        display: block;
      }

      .markdown :where(h1, h2, h3, h4, h5, h6) {
        font-weight: bold;
        margin: 1em 0 0.5em;
      }

      .markdown :where(p, ul, ol, pre, blockquote) {
        margin: 0.5em 0;
      }

      .markdown :where(code) {
        font-family: var(--sl-font-mono, monospace);
        background: transparent;
        padding: 0.2em 0.4em;
        border-radius: 4px;
      }

      .markdown :where(a) {
        color: inherit;
        text-decoration: underline;
      }
    `;

    this.shadowRoot.append(style, this.container);
  }

  connectedCallback() {
    this.renderMarkdown();
  }

  renderMarkdown() {
    const raw = this.textContent.trim();
    const html = this.md.render(raw);
    this.container.innerHTML = html;

    this.dispatchEvent(
      new CustomEvent("content-updated", {
        bubbles: true,
        composed: true,
      })
    );
  }
}

customElements.define("s-markdown", SMarkdown);
