const fs = require("fs");
const path = require("path");

const babel = require("@babel/core");
const t = require("@babel/types");

// TODO: take file paths via CLI
const result = babel.transformFileSync(path.join('./input.js') , {
    plugins: [
      // TODO: turn each AST transform into proper Babel plugin
      path.join(__dirname, 'plugin_eval_expr.js')
    ]
});

fs.writeFileSync(path.join(__dirname, 'output.js'), result.code, 'utf-8');
