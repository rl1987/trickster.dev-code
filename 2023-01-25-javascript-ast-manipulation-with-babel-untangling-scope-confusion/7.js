export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      FunctionDeclaration(path) {
        let fnName = path.node.id.name;
        let binding = path.scope.getBinding(fnName);
        if (!binding.referenced) path.remove();
      }
    }
  };
}

