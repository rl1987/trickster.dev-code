const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "undo-object-tostring-call", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        let callee = node.callee;
        if (!t.isMemberExpression(callee)) return;
        let calleeObj = callee.object;
        if (!t.isMemberExpression(calleeObj)) return;
        if (!t.isCallExpression(calleeObj.object)) return;
        calleeObj = calleeObj.object;
        if (!t.isIdentifier(calleeObj.callee)) return;
        if (calleeObj.callee.name != "Object") return;
        if (!t.isStringLiteral(callee.property)) return;
        if (callee.property.value != "call") return;
        if (!t.isStringLiteral(callee.object.property)) return;
        if (callee.object.property.value != "toString") return;
        let newNode = t.valueToNode(Object()["toString"]["call"]());
        logASTChange("undo-object-tostring-call", node, newNode);
        path.replaceWith(newNode);
      }
    }
  };
}
