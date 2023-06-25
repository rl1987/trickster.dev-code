const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
  return {
    name: "simplify-string-name", // not required
    visitor: {
      MemberExpression(path) {
        let node = path.node;
        if (!t.isIdentifier(node.object)) return;
        if (!t.isStringLiteral(node.property)) return;
        if (node.object.name === "String" && node.property.value === "name") {
          path.replaceWith(t.valueToNode("String"));
        }
      }
    }
  };
}
