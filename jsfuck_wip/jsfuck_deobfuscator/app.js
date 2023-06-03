const fs = require("fs");
const path = require("path");

const babel = require("@babel/core");
const t = require("@babel/types");

// TODO: take file paths via CLI
let js = fs.readFileSync("./input.js", "utf-8");
console.log(js);
console.log("-----------------------------------------------------------------");

while (true) {
  const result = babel.transformSync(js, {
      plugins: [
        // TODO: turn each AST transform into proper Babel plugin
        path.join(__dirname, 'plugin_eval_expr.js'),
        path.join(__dirname, 'plugin_undo_flat_trick.js'),
        path.join(__dirname, 'plugin_undo_entries_trick.js'),
        path.join(__dirname, 'plugin_undo_concat_trick.js'),
        path.join(__dirname, 'plugin_undo_slice_trick.js'),
        path.join(__dirname, 'plugin_undo_boolean_trick.js'),
        path.join(__dirname, 'plugin_undo_fontcolor_trick.js'),
        path.join(__dirname, 'plugin_undo_italics_trick.js'),
        path.join(__dirname, 'plugin_undo_function_escape_trick.js'),
        path.join(__dirname, 'plugin_undo_function_date_trick.js'),
        path.join(__dirname, 'plugin_undo_regexp_trick.js'),
        path.join(__dirname, 'plugin_undo_string_trick.js'),
        path.join(__dirname, 'plugin_undo_number_tostring_trick.js'),
        path.join(__dirname, 'plugin_undo_object_tostring_trick.js')
      ]
  });

  if (result.code == js) break;

  console.log(result.code);
  console.log("-----------------------------------------------------------------");

  js = result.code;
}

fs.writeFileSync(path.join(__dirname, 'output.js'), js, 'utf-8');
