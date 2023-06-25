export default function (babel) {
  const { types: t } = babel;

  return {
    name: "string-array-join", // not required
    visitor: {
      CallExpression(path) {
        const callExpr = path.node;
        const memberExpr = callExpr.callee;
        if (!t.isMemberExpression(memberExpr)) return;
        let array = memberExpr.object;
        if (!t.isArrayExpression(array)) return;
        if (array.elements.length == 0) return;
        array = array.elements;

        for (let i = 0; i < array.length; i++) {
          const element = array[i];
          if (!t.isStringLiteral(element))
            return;
          
          array[i] = element.value;
        }
                
        const fnName = memberExpr.property;
        if (!t.isStringLiteral(fnName)) return;
        if (fnName.value != "join") return;
        
        if (callExpr.arguments.length != 1) return;
        
        let separator = callExpr.arguments[0];
        if (!t.isStringLiteral(separator)) return;
        separator = separator.value;
        
        let newNode = t.stringLiteral(array.join(separator));
        path.replaceWith(newNode);
      }
    }
  };
}
