const generate = require("@babel/generator").default;

function logASTChange(pluginName, ast1, ast2) {
  const js1 = generate(ast1).code;
  const js2 = generate(ast2).code;

  console.log("PLUGIN NAME:", pluginName);
  console.log("FROM CODE:", js1);
  console.log("TO CODE:", js2);
}

module.exports = { logASTChange };
