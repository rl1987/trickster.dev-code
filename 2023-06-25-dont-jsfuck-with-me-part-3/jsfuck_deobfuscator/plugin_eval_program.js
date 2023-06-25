const babel = require("@babel/core");
const t = require("@babel/types");
const parser = require("@babel/parser");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "eval-program", // not required
    visitor: {
      Program(path) {
        let program = path.node;
        let body = program.body;
        if (body.length != 1) return;
        if (!t.isExpressionStatement(body[0])) return;
        let callExpr = body[0].expression;
        if (!t.isCallExpression(callExpr)) return;
    		if (!t.isIdentifier(callExpr.callee)) return;
        if (callExpr.callee.name != "eval") return;
        if (callExpr.arguments.length != 1) return;
        let jsStr = callExpr.arguments[0];
        if (!t.isStringLiteral(jsStr)) return;
        jsStr = jsStr.value;
        
        let parsed = parser.parse(jsStr); // File node
        logASTChange("eval-program", program, parsed.program);
        path.replaceWith(parsed.program);
      }
    }
  };
}
