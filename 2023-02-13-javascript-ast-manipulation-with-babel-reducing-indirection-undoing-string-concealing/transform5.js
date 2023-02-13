function decode(_0x5d79db, _0x4ad0a1) {
  const _0x150e0f = ['yxbPlM5PA2uUy29T', 'kI8Q', 'zw4Tr0iSzw4Tvvm7Ct0WlJKSzw47Ct0WlJG', 'Ahr0Chm6lY93D3CUBMLRzs5JB20', 'Ahr0Chm6lY93D3CUBMLRzs5JB20V', 'iM1Hy09tiG', 'zw1WDhK', 'y29YCW', 'ANnVBG', 'Bg9N'];

  decode = function (_0x2ee979, _0x4a74f2) {
    _0x2ee979 = _0x2ee979 - 0x0;
    let _0x299466 = _0x150e0f[_0x2ee979];

    if (decode['sjCySo'] === undefined) {
      var _0x1cb49b = function (_0x307ab8) {
        const base64Alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';
        let _0x19f00a = '';
        let _0xf75b57 = '';

        for (let _0x1806d0 = 0x0, _0x425bd6, _0x1bc5e5, _0x152116 = 0x0; _0x1bc5e5 = _0x307ab8['charAt'](_0x152116++); ~_0x1bc5e5 && (_0x425bd6 = _0x1806d0 % 0x4 ? _0x425bd6 * 0x40 + _0x1bc5e5 : _0x1bc5e5, _0x1806d0++ % 0x4) ? _0x19f00a += String['fromCharCode'](0xff & _0x425bd6 >> (-0x2 * _0x1806d0 & 0x6)) : 0x0) {
          _0x1bc5e5 = base64Alphabet['indexOf'](_0x1bc5e5);
        }

        for (let _0x4858d8 = 0x0, _0x24c07d = _0x19f00a['length']; _0x4858d8 < _0x24c07d; _0x4858d8++) {
          _0xf75b57 += '%' + ('00' + _0x19f00a['charCodeAt'](_0x4858d8)['toString'](0x10))['slice'](-0x2);
        }

        return decodeURIComponent(_0xf75b57);
      };

      decode['rQzPwo'] = _0x1cb49b;
      _0x5d79db = arguments;
      decode['sjCySo'] = !![];
    }

    const _0x29a87a = _0x150e0f[0x0];
    const response = _0x2ee979 + _0x29a87a;
    const json = _0x5d79db[response];

    if (!json) {
      _0x299466 = decode['rQzPwo'](_0x299466);
      _0x5d79db[response] = _0x299466;
    } else {
      _0x299466 = json;
    }

    return _0x299466;
  };

  return decode(_0x5d79db, _0x4ad0a1);
}

export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (node.callee.name != "decode") return;
        if (!node.arguments) return;
        if (node.arguments.length != 1) return;
        let arg = node.arguments[0].value;
        let decodedStr = decode(arg);
        path.replaceWith(t.valueToNode(decodedStr));
      },
      FunctionDeclaration(path) {
        if (path.node.id.name === "decode") path.remove();
      }
    }
  };
}
