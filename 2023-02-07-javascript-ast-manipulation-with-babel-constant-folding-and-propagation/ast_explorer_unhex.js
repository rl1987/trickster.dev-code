export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      NumericLiteral(path) {
        if (path.node.extra.raw.startsWith("0x")) delete path.node.extra.raw;
      },
    }
  };
}

