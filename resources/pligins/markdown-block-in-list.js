const container = require("markdown-it-container");

module.exports = function markdownItBlock(md) {
  // block コンテナを登録
  md.use(container, "block", {
    marker: ":",
    validate: function (params) {
      return params.trim().match(/^block\s*$/);
    },
    render(tokens, idx) {
      const token = tokens[idx];
      return token.nesting === 1 ? '<div class="block">\n' : "</div>\n";
    },
  });

  // block の中身を再パースして Markdown として解釈
  const originalRender = md.renderer.render;
  md.renderer.render = function (tokens, options, env) {
    const newTokens = [];
    for (let i = 0; i < tokens.length; i++) {
      const token = tokens[i];

      if (token.type === "container_block_open") {
        newTokens.push(token);

        // block の中身を収集
        let content = "";
        i++;
        while (
          i < tokens.length &&
          tokens[i].type !== "container_block_close"
        ) {
          const t = tokens[i];
          if (t.type === "fence" || t.type === "code_block") {
            content += "```\n" + t.content + "\n```\n";
          } else {
            content += t.content + "\n";
          }
          i++;
        }

        // 再パース
        const nestedMd = new md.constructor();
        nestedMd.use(container, "block"); // block の中で block を使いたい場合
        const nestedTokens = nestedMd.parse(content.trim(), env);
        newTokens.push(...nestedTokens);

        // 閉じタグ
        newTokens.push(tokens[i]);
      } else {
        newTokens.push(token);
      }
    }

    return originalRender.call(this, newTokens, options, env);
  };
};
