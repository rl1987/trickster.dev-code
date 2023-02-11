function decode(_0x5d79db, _0x4ad0a1) {
  const _0x150e0f = ['yxbPlM5PA2uUy29T', 'kI8Q', 'zw4Tr0iSzw4Tvvm7Ct0WlJKSzw47Ct0WlJG', 'Ahr0Chm6lY93D3CUBMLRzs5JB20', 'Ahr0Chm6lY93D3CUBMLRzs5JB20V', 'iM1Hy09tiG', 'zw1WDhK', 'y29YCW', 'ANnVBG', 'Bg9N']();

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

(async () => {
  try {
    const response = await fetch('https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=A7CA2A92E0F04E570767C7810552BBC5&country=au&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(AU)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(8529ff38-7de8-4f69-973c-9fdbfb102ed2%2C16633190-45e5-4830-a068-232ac7aea82c)%26anchor%3D24%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D', {
      'headers': {
        'authority': decode(0),
        'accept': decode(1),
        'accept-language': decode(2),
        'cache-control': 'no-cache',
        'origin': decode(3),
        'pragma': 'no-cache',
        'referer': decode(4),
        'sec-ch-ua': '\x22Not_A\x20Brand\x22;v=\x2299\x22,\x20\x22Google\x20Chrome\x22;v=\x22109\x22,\x20\x22Chromium\x22;v=\x22109\x22',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': decode(5),
        'sec-fetch-dest': decode(6),
        'sec-fetch-mode': decode(7),
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0\x20(Macintosh;\x20Intel\x20Mac\x20OS\x20X\x2010_15_7)\x20AppleWebKit/537.36\x20(KHTML,\x20like\x20Gecko)\x20Chrome/109.0.0.0\x20Safari/537.36'
      }
    });
    const json = await response[decode(8)]();
    console['log'](json);
  } catch (_0x307ab8) {
    console[decode(9)](_0x307ab8);
  }
})();
