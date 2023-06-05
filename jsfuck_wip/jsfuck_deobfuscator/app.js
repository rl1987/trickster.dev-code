const fs = require("fs");
const path = require("path");
const process = require("process");

const babel = require("@babel/core");
const t = require("@babel/types");

if (process.argv.length != 4) {
  console.log("Usage:");
  console.log("node app.js <input_js> <output_js>");
  process.exit(0);
}

const input_js = process.argv[2];
const output_js = process.argv[3];

let js = fs.readFileSync(input_js, "utf-8");
console.log(js);
console.log("-----------------------------------------------------------------");

while (true) {
  const result = babel.transformSync(js, {
      plugins: [
        path.join(__dirname, 'plugin_eval_expr.js'),
        path.join(__dirname, 'plugin_undo_flat_trick.js'),
        path.join(__dirname, 'plugin_undo_entries_trick.js'),
        path.join(__dirname, 'plugin_undo_concat_trick.js'),
        path.join(__dirname, 'plugin_undo_slice_trick.js'),
        path.join(__dirname, 'plugin_undo_boolean_trick.js'),
        path.join(__dirname, 'plugin_undo_fontcolor_trick.js'),
        path.join(__dirname, 'plugin_undo_italics_trick.js'),
        path.join(__dirname, 'plugin_undo_function_escape_trick.js'),
        path.join(__dirname, 'plugin_undo_escape_call.js'),
        path.join(__dirname, 'plugin_undo_function_date_trick.js'),
        path.join(__dirname, 'plugin_undo_regexp_trick.js'),
        path.join(__dirname, 'plugin_undo_string_trick.js'),
        path.join(__dirname, 'plugin_undo_number_tostring_trick.js'),
        path.join(__dirname, 'plugin_undo_object_tostring_trick.js'),
        path.join(__dirname, 'plugin_eval_return_str.js'),
        path.join(__dirname, 'plugin_eval_return_fncall.js'),
        path.join(__dirname, 'plugin_fix_eval.js'),
        path.join(__dirname, 'plugin_constructor_str.js'),
        path.join(__dirname, 'plugin_refactor_regex_constr.js'),
        path.join(__dirname, 'plugin_regex_str.js'),
        path.join(__dirname, 'plugin_simplify_false_regex.js'),
        path.join(__dirname, 'plugin_string_array_join.js'),
        path.join(__dirname, 'plugin_string_constructor_name.js'),
        path.join(__dirname, 'plugin_string_split.js')
      ]
  });

  if (result.code == js) break;

  console.log(result.code);
  console.log("-----------------------------------------------------------------");

  js = result.code;
}

fs.writeFileSync(path.join(__dirname, output_js), js, 'utf-8');
