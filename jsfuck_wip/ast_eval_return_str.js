export default function (babel) {
  const { types: t } = babel;

  return {
    name: "eval-return-str", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (!t.isIdentifier(node.callee)) return;
        if (node.callee.name != "eval") return;
        if (node.arguments.length != 1) return;
        if (!t.isStringLiteral(node.arguments[0])) return;
        
        let argStr = node.arguments[0].value;
        
        if (argStr.startsWith("return\"") && argStr.endsWith("\"")) {
          argStr = argStr.substr("return\"".length);
          argStr = argStr.substr(0, argStr.length-1);
          // HACK to deal with escaped characters.
          // https://stackoverflow.com/questions/48030856/evaluating-escaped-string-literals-in-javascript
          argStr = eval('"' + argStr + '"')
          path.replaceWith(t.stringLiteral(argStr));
        }
      }
    }
  };
}
