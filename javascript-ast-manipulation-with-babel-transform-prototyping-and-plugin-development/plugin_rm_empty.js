const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
    return {
        name: "rm_needless_semicolons",
        visitor: {
            EmptyStatement: function (path) {
                path.remove();
            }
        }
    }
};
