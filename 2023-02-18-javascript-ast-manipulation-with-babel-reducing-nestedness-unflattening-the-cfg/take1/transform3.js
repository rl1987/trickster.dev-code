export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      FunctionDeclaration(path) {
        let node = path.node;
        if (!node.id) return;
        let scope = path.scope;
        let binding = scope.getBinding(node.id.name);
        if (!binding.referenced) path.remove();
      },
      EmptyStatement(path) {
        path.remove();
      }
    }
  };
}