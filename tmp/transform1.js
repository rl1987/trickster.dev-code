export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      VariableDeclarator(path) {
        let node = path.node;
        if (!node.init) return;
        if (node.init.type != "ObjectExpression") return;
        let binding = path.scope.getBinding(node.id.name);
        if (!binding.constant) return;
        console.log(binding);
        let properties = node.init.properties;
        if (!properties) return;
        
        let kv = new Object();
        
        for (let prop of properties) {
          if (!t.isIdentifier(prop.key)) return;
          let key = prop.key.name;
          if (!t.isLiteral(prop.value)) return;
          let value = prop.value.value;
          kv[key] = value;
        }
        
        for (let refPath of binding.referencePaths) {
          if (!refPath.parentPath) return;
          let parentNode = refPath.parentPath.node;
          if (!t.isMemberExpression(parentNode)) return;
          let key = parentNode.property.name;
          let value = kv[key];
          refPath.parentPath.replaceWith(t.valueToNode(value));
        }
        
        path.remove();
      } 
    }
  };
}