export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      Program(path) {
        console.log(path.scope);
      }
    }
  };
}

