# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'museums.middlewares.BrightDataDownloaderMiddleware': 500,
}