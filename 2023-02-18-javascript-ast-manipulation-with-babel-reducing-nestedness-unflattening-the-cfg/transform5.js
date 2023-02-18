export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      VariableDeclarator(path) {
        let node = path.node;
        let init = node.init;
        if (!init || !t.isCallExpression(init)) return;
        let callee = init.callee;
        let obj = callee.object;
        if (!t.isStringLiteral(obj)) return;
        let prop = callee.property;
        if (!t.isIdentifier(prop)) return;
        if (prop.name != "split") return;
        let args = init.arguments;
        if (args.length != 1) return;
        if (!t.isStringLiteral(args[0])) return;

        let strToSplit = obj.value;
        let separator = args[0].value;
        
        let components = strToSplit.split(separator).map(t.valueToNode);
        
        node.init = t.arrayExpression(components);
      }
    }
  };
}