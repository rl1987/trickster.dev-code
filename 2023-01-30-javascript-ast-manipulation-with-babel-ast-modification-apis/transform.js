export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      FunctionDeclaration(path) {
        let body = path.get('body');
        body.unshiftContainer('body', t.debuggerStatement());
        body.pushContainer('body', t.debuggerStatement());
      }
    }
  };
}

