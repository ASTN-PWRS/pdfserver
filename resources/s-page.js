class SPage extends HTMLElement {
  static get observedAttributes() {
    return ["size", "direction", "debug"];
  }

  constructor() {
    super();
    this.attachShadow({ mode: "open" });

    this.sizeMap = {
      A3: { width: 297, height: 420 },
      A4: { width: 210, height: 297 },
      A5: { width: 148, height: 210 },
      B5: { width: 182, height: 257 },
    };

    this.content = document.createElement("div");
    this.content.className = "page";
    this.content.setAttribute("part", "content");

    const slot = document.createElement("slot");
    this.content.appendChild(slot);

    // ⚠ 透かし要素
    this.watermark = document.createElement("div");
    this.watermark.className = "watermark";
    this.watermark.textContent = "⚠ サイズオーバー";
    this.watermark.style.display = "none";
    this.content.appendChild(this.watermark);

    const style = document.createElement("style");
    style.textContent = `
      .page {
        position: relative;
        background: white;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        overflow: hidden;
        margin: 0;
      }

      .page.debug {
        background-color: rgba(0, 0, 0, 0.03);
      }

      :host-context(.sl-theme-dark) .page.debug {
        background-color: rgba(255, 255, 255, 0.05);
      }

      .watermark {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-20deg);
        font-size: 3rem;
        color: rgba(200, 0, 0, 0.9);
        pointer-events: none;
        white-space: nowrap;
        user-select: none;
        z-index: 0;
      }
    `;

    this.shadowRoot.append(style, this.content);
  }

  connectedCallback() {
    if (!this.hasAttribute("size")) this.setAttribute("size", "A4");
    if (!this.hasAttribute("direction"))
      this.setAttribute("direction", "portrait");

    this.updateSize();
    this.observeResize();
    this.updateDebugStyle();

    requestAnimationFrame(() => this.checkOverflow());

    this.addEventListener("content-updated", () => this.checkOverflow());
  }

  attributeChangedCallback(name) {
    if (name === "size" || name === "direction") this.updateSize();
    if (name === "debug") this.updateDebugStyle();
  }

  updateSize() {
    const size = this.getAttribute("size") || "A4";
    const direction = this.getAttribute("direction") || "portrait";
    const { width, height } = this.sizeMap[size] || this.sizeMap["A4"];
    const w = direction === "portrait" ? width : height;
    const h = direction === "portrait" ? height : width;

    this.content.style.width = `${w}mm`;
    this.content.style.height = `${h}mm`;

    this.checkOverflow();
  }

  updateDebugStyle() {
    this.content.classList.toggle("debug", this.hasAttribute("debug"));
  }

  observeResize() {
    this.resizeObserver = new ResizeObserver(() => this.checkOverflow());
    this.resizeObserver.observe(this.content);
  }

  checkOverflow() {
    const el = this.content;
    const style = getComputedStyle(el);

    const paddingTop = parseFloat(style.paddingTop);
    const paddingBottom = parseFloat(style.paddingBottom);
    const paddingLeft = parseFloat(style.paddingLeft);
    const paddingRight = parseFloat(style.paddingRight);

    const borderTop = parseFloat(style.borderTopWidth);
    const borderBottom = parseFloat(style.borderBottomWidth);
    const borderLeft = parseFloat(style.borderLeftWidth);
    const borderRight = parseFloat(style.borderRightWidth);

    const innerWidth =
      el.clientWidth - paddingLeft - paddingRight - borderLeft - borderRight;
    const innerHeight =
      el.clientHeight - paddingTop - paddingBottom - borderTop - borderBottom;

    const contentWidth = el.scrollWidth;
    const contentHeight = el.scrollHeight;

    const over = contentWidth > innerWidth || contentHeight > innerHeight;

    this.watermark.style.display = over ? "block" : "none";
  }

  disconnectedCallback() {
    this.resizeObserver?.disconnect();
  }
}

customElements.define("s-page", SPage);
