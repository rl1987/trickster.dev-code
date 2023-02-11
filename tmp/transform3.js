const betterNames = {
  "_0x4ad0": "decode",
  "_0x3d5a8f": "encodedStrings",
  "_0x5d79": "getEncodedStrings",
  "_0x4d32cc": "base64Alphabet",
  "_0x23768c": "response",
  "_0x1499a9": "json"
};

export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      Identifier(path) {
        let name = path.node.name;
        if (name in betterNames) {
          let newName = betterNames[name];
          let newIdentifier = t.identifier(newName);
          
          let scope = path.scope;
          let binding = scope.getBinding(name);
          
          for (let refPath of binding.referencePaths) {
            refPath.replaceWith(newIdentifier);
          }
          
          path.replaceWith(newIdentifier);
        }
      }
    }
  };
}