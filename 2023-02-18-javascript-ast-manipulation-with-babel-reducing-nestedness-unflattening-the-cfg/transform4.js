export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      VariableDeclarator(path) {
        let idName = path.node.id.name;
        let parentScope = path.scope.parent;
        if (!parentScope) return;
        if (parentScope.getBinding(idName)) {
          let newName = path.scope.generateUidIdentifier(idName);
          path.scope.rename(idName, newName.name);
        }
      }
    }
  };
}