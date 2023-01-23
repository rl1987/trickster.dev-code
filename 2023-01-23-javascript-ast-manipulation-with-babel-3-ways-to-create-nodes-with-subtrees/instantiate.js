const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const t = require("@babel/types");

const debugStmt1 =  t.debuggerStatement();

const consoleId = t.identifier("console");
const logId = t.identifier("log");
const stringLiteral = t.stringLiteral("!");
const callee = t.memberExpression(consoleId, logId);
const callExpr = t.callExpression(callee, [ stringLiteral ]);
const exprStmt = t.expressionStatement(callExpr);

const debugStmt2 =  t.debuggerStatement();

const body = [ debugStmt1, exprStmt, debugStmt2 ];

const ast = parser.parse(""); // Parsing empty string creates AST with File and Program nodes.

ast.program.body = body;

console.log(ast);
console.log("==================");
console.log(generate(ast).code);

