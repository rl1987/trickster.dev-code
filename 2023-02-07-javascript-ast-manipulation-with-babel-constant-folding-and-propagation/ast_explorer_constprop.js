export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      VariableDeclarator(path) {
        if (path.node.init == null) return;
        if (!t.isLiteral(path.node.init)) return;
        const binding = path.scope.getBinding(path.node.id.name);
        if (!binding.constant) return;
        for (let i = 0; i < binding.referencePaths.length; i++) {
          let refPath = binding.referencePaths[i];
          refPath.replaceWith(path.node.init);
        }
        path.remove();
      } 
    }
  };
}

