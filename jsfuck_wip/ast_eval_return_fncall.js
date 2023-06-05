export default function (babel) {
  const { types: t } = babel;

  return {
    name: "eval-return-fncall", // not required
    visitor: {
      CallExpression(path) {
        let callExpr = path.node;
        let callExpr2 = callExpr.callee;
        if (!t.isCallExpression(callExpr2)) return;
        
        if (!t.isIdentifier(callExpr2.callee)) return;
        if (callExpr2.callee.name != "eval") return;
        if (callExpr2.arguments.length != 1) return;
        if (!t.isStringLiteral(callExpr.arguments[0])) return;
        if (!t.isStringLiteral(callExpr2.arguments[0])) return;

        let argStr = callExpr2.arguments[0].value;
        console.log(argStr);
        
        if (argStr.startsWith("return ") && !argStr.includes('"')) {
          let fnName = argStr.substr("return ".length)
          console.log(fnName);
          let newNode = t.callExpression(t.identifier(fnName), 
                                         [t.cloneNode(callExpr.arguments[0])]);
          
          path.replaceWith(newNode);
          if (fnName == "eval") path.skip();
        }
      }
    }
  };
}
