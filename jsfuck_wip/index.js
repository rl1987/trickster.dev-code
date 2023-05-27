const fs = require("fs");
const path = require("path");

const babel = require("@babel/core");
const t = require("@babel/types");

// TODO: take file paths via CLI
const result = babel.transformFileSync(path.join(__dirname, 'input.js') , {
    plugins: [
      // TODO: turn each AST transform into proper Babel plugin
    ]
});

console.log(result.code);

fs.writeFileSync(path.join(__dirname, 'output.js'), result.code, 'utf-8');
