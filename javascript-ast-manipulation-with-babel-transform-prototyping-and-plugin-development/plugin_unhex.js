const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
    return {
        name: "undo_hexadecimal_strings",
        visitor: {
            StringLiteral: function (path) {
                path.node.extra.raw = '"' + path.node.extra.rawValue + '"';
            }
        }
    }
};
