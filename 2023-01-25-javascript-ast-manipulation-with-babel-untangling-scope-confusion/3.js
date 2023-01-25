export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      VariableDeclarator(path) {
        if (path.node.id.name == "y") {
          console.log(path.scope);
          console.log("PARENT", path.scope.parent);
        }
      }
    }
  };
}

