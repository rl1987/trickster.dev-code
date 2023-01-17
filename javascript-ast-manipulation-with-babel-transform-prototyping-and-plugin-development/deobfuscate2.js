const fs = require("fs");
const path = require("path");

const babel = require("@babel/core");
const t = require("@babel/types");

const result = babel.transformFileSync(path.join(__dirname, 'input.js') , {
    plugins: [
        path.join(__dirname, 'plugin_unhex.js'),
        path.join(__dirname, 'plugin_unbracket.js'),
        path.join(__dirname, 'plugin_rm_empty.js')
    ]
});

console.log(result.code);

fs.writeFileSync(path.join(__dirname, 'output.js'), result.code, 'utf-8');

