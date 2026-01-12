class SPage extends HTMLElement {
  static get observedAttributes() {
    return ["size", "direction"];
  }

  constructor() {
    super();
    this.attachShadow({ mode: "open" });

    // サイズ定義（mm単位）
    this.sizeMap = {
      A3: { width: 297, height: 420 },
      A4: { width: 210, height: 297 },
      A5: { width: 148, height: 210 },
      B5: { width: 182, height: 257 },
    };

    // 要素の作成
    this.wrapper = document.createElement("div");
    this.wrapper.className = "page";

    const slot = document.createElement("slot");
    this.wrapper.appendChild(slot);

    this.overlay = document.createElement("div");
    this.overlay.className = "overlay";
    this.overlay.textContent = "⚠ サイズオーバー";

    const style = document.createElement("style");
    style.textContent = `
      .page {
        background: white;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        overflow: hidden;
        position: relative;
        margin: auto;
      }
      .overlay {
        position: absolute;
        inset: 0;
        background: rgba(255, 0, 0, 0.1);
        color: red;
        font-weight: bold;
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 10;
        pointer-events: none;
        font-size: 1.2rem;
      }
    `;

    this.shadowRoot.append(style, this.wrapper, this.overlay);
  }

  connectedCallback() {
    // デフォルト値を設定（属性が未指定の場合）
    if (!this.hasAttribute("size")) {
      this.setAttribute("size", "A4");
    }
    if (!this.hasAttribute("direction")) {
      this.setAttribute("direction", "portrait");
    }
    this.updateSize();
    this.observeResize();
    this.addEventListener("content-updated", () => this.checkOverflow());
  }

  attributeChangedCallback() {
    this.updateSize();
  }

  updateSize() {
    const size = this.getAttribute("size") || "A4";
    const direction = this.getAttribute("direction") || "portrait";
    const { width, height } = this.sizeMap[size] || this.sizeMap["A4"];

    const w = direction === "portrait" ? width : height;
    const h = direction === "portrait" ? height : width;

    this.wrapper.style.width = `${w}mm`;
    this.wrapper.style.height = `${h}mm`;

    this.checkOverflow();
  }

  observeResize() {
    this.resizeObserver = new ResizeObserver(() => this.checkOverflow());
    this.resizeObserver.observe(this.wrapper);
  }

  checkOverflow() {
    const el = this.wrapper;
    const over =
      el.scrollHeight > el.clientHeight || el.scrollWidth > el.clientWidth;
    this.overlay.style.display = over ? "flex" : "none";
  }

  disconnectedCallback() {
    this.resizeObserver?.disconnect();
  }
}

customElements.define("s-page", SPage);
