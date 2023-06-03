const fs = require("fs");
const path = require("path");

const babel = require("@babel/core");
const t = require("@babel/types");

// TODO: take file paths via CLI
let js = fs.readFileSync("./input.js", "utf-8");
console.log(js);
console.log("-----------------------------------------------------------------");

while (true) {
  const result = babel.transformSync(js, {
      plugins: [
        // TODO: turn each AST transform into proper Babel plugin
        path.join(__dirname, 'plugin_eval_expr.js')
      ]
  });

  if (result.code == js) break;

  console.log(result.code);
  console.log("-----------------------------------------------------------------");

  js = result.code;
}

fs.writeFileSync(path.join(__dirname, 'output.js'), js, 'utf-8');
