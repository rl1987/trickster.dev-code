const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const t = require("@babel/types");
const template = require("@babel/template").default;

const exampleTempl = template(`
debugger;
console.log(%%msg%%);
debugger;
`);

const body = exampleTempl({
    msg: t.stringLiteral("!")
});

const ast = parser.parse("");

ast.program.body = body;

console.log(ast);
console.log("==================");
console.log(generate(ast).code);

