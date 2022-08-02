const fs = require("fs");

const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;

let js = fs.readFileSync("quotes.js", "utf-8");

const ast = parser.parse(js);

var rows = [];

traverse(ast, {
    ArrayExpression: function(path) {
        let arrayNode = path.node;
        for (idx  = 0; idx < arrayNode.elements.length; idx++) {
            let node = arrayNode.elements[idx];
            var row = {};

            if (node.properties === undefined)
                continue;

            for (i = 0; i < node.properties.length; i++) {
                let property = node.properties[i];
                if (property.key.value == "text") {
                    row["text"] = property.value.value;
                } else if (property.key.value == "author") {
                    let author_properties = property.value.properties;

                    for (j = 0; j < author_properties.length; j++) {
                        let author_property = author_properties[j];
                        if (author_property.key.value == "name") {
                            row["author_name"] = author_property.value.value;
                        }
                    }
                }
            }

            rows.push(row);
        }
    }
});

console.log(rows);
