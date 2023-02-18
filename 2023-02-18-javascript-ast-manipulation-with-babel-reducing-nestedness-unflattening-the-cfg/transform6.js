export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      WhileStatement(path) {
        let whileStmt = path.node;
        let parentBody = path.parent.body;
        let bodyBlock = whileStmt.body;
        let bodyParts = bodyBlock.body;
        if (bodyParts.length == 0) return;
        if (!t.isSwitchStatement(bodyParts[0])) return;
        let switchStmt = bodyParts[0];
        let switchCases = switchStmt.cases;
        
        let basicBlocksByCase = {};
        
        for (let switchCase of switchCases) {
          let key = switchCase.test.value;
          basicBlocksByCase[key] = switchCase.consequent;
        }
        
        let arrayName = switchStmt.discriminant.object.name;
        let parentScope = path.parentPath.scope;
        let binding = parentScope.getBinding(arrayName);
        
        let arrayExpr = binding.path.node.init;
        let order = arrayExpr.elements.map((stringLiteral) => stringLiteral.value)
      
        let stuffInOrder = [];
        
        for (let caseNum of order) {
          let basicBlock = basicBlocksByCase[caseNum];
          stuffInOrder.push(...basicBlock); // https://stackoverflow.com/a/1374131/1044147
        }
        
        path.replaceWithMultiple(stuffInOrder);
        binding.path.remove();
      },
      ContinueStatement(path) {
        path.remove();
      }
    }
  };
}