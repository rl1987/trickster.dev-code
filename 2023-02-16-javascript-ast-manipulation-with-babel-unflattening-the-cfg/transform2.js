export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      TryStatement(path) {
        let node = path.node;
        let catchClause = node.handler;
        if (!catchClause) return;
        let catchBody = catchClause.body.body;
        if (!catchBody.length === 0) return;
        
        let firstCatchLine = catchBody[0];
        if (t.isExpressionStatement(firstCatchLine)) {
          if (t.isAssignmentExpression(firstCatchLine.expression)) {
            let assigmentExpr = firstCatchLine.expression;
          	if (t.isIdentifier(assigmentExpr.left) && 
                assigmentExpr.left.name === "$$defendjs$tobethrown") {
              let tryBody = node.block.body;
              path.replaceWithMultiple(tryBody);
            }
          }
        }
      }
    }
  };
}