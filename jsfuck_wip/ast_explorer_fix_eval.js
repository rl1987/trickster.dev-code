export default function (babel) {
  const { types: t } = babel;

  return {
    name: "fix-eval", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        let parent = path.parent;
        if (!t.isCallExpression(parent)) return;
        let callee = node.callee;
        if (!t.isMemberExpression(callee)) return;
        if (!t.isStringLiteral(callee.property)) return;
        let key1 = callee.property.value;
        if (!t.isMemberExpression(callee.object)) return;
        if (!t.isStringLiteral(callee.object.property)) return;
        let key2 = callee.object.property.value;
        if (key1 === "constructor" && (key2 === "filter" || key2 === "flat")) {
          let evalCallExpr = t.callExpression(t.identifier('eval'), 
                                                           node.arguments);
          path.parentPath.replaceWith(evalCallExpr);
        }
      }
    }
  };
}
