export default function (babel) {
const { types: t } = babel;

 return {
    name: "number-constructor-str", // not required
    visitor: {
      MemberExpression(path) {
        const node = path.node;
        let obj = node.object;
        if (!t.isNumericLiteral(obj)) return;
		let property = node.property;
        if (!t.isStringLiteral(property)) return;
        if (property.value != "constructor") return;
        if (!t.isBinaryExpression(path.parent)) return;
        
        path.replaceWith(t.stringLiteral(String(Number.prototype.constructor)));
      }
    }
  };
}
