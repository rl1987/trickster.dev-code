export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      VariableDeclarator(path) {
        let node = path.node;
        if (!node.init) return;
        if (!t.isIdentifier(node.init)) return;
        let scope = path.scope;
        let binding = scope.getBinding(node.id.name);
        
        for (let refPath of binding.referencePaths) {
          refPath.replaceWith(node.init);
        }
        path.remove();
      } 
    }
  };
}
