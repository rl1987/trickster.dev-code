(async () => {
  try {
    const response = await fetch('https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=A7CA2A92E0F04E570767C7810552BBC5&country=au&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(AU)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(8529ff38-7de8-4f69-973c-9fdbfb102ed2%2C16633190-45e5-4830-a068-232ac7aea82c)%26anchor%3D24%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D', {
      headers: {
        'authority': 'api.nike.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://www.nike.com',
        'pragma': 'no-cache',
        'referer': 'https://www.nike.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
      }
    });
    const json = await response.json()
    console.log(json);
  } catch (error) {
    console.log(error);
  }
})();
