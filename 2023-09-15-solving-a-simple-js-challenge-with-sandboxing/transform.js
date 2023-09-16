export default function (babel) {
  const { types: t } = babel;
  
  return {
    name: "ast-transform", // not required
    visitor: {
      "Program|IfStatement|Expression|ExpressionStatement"(path) {
        t.removeComments(path.node);
      }
    }
  };
}

