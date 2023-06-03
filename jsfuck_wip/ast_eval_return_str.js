// Based on code from: https://stackoverflow.com/a/62633125
function decodeUnicodeChar(str) {
  if (str == null) return ""; // no need extra test on undefined
  var r = /\\u([\d\w]{4})/gi;
  var r3 = /\\([\d\w]{3})/gi;
  var r2 = /\\([\d\w]{2})/gi;

  str = str.replace(r, (match, grp) => String.fromCharCode(parseInt(grp, 16)))
           .replace(r3, (match, grp) => String.fromCharCode(parseInt(grp, 8)))
           .replace(r2, (match, grp) => String.fromCharCode(parseInt(grp, 8)));

  return str; // return it
}

export default function (babel) {
  const { types: t } = babel;

  return {
    name: "eval-return-str", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (!t.isIdentifier(node.callee)) return;
        if (node.callee.name != "eval") return;
        if (node.arguments.length != 1) return;
        if (!t.isStringLiteral(node.arguments[0])) return;
        
        let argStr = node.arguments[0].value;
        
        if (argStr.startsWith("return\"") && argStr.endsWith("\"")) {
          argStr = argStr.substr("return\"".length);
          argStr = argStr.substr(0, argStr.length-1);
          argStr = decodeUnicodeChar(argStr);
          path.replaceWith(t.stringLiteral(argStr));
        }
      }
    }
  };
}
