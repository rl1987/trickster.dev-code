const fs = require("fs");

const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;

let js = fs.readFileSync("fb_example.js", "utf-8");

const ast = parser.parse(js);

var url = null;

traverse(ast, {
    ObjectProperty: function(path) {
        if (!path.node.method && path.node.key.name == "href") {
            url = path.node.value.value;
        }
    }
});

console.log(url);
