const fs = require("fs");
const vm = require("vm");

let js = fs.readFileSync("in.js", "utf-8");

const script = new vm.Script(js);
const mapperContext = { window: {}, document: {
  location: {
    reload: function(){}
  }
}};

const sandbox = vm.createContext(mapperContext);
script.runInContext(sandbox);
vm.runInContext('go();', sandbox);

console.log(sandbox.document.cookie);
