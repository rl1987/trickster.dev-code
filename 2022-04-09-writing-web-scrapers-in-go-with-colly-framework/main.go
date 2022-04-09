package main

import (
	"fmt"

	"github.com/gocolly/colly"
)

type Book struct {
	Title        string
	Description  string
	UPC          string
	PriceExclTax float64
	PriceInclTax float64
	Tax          float64
	Availability string
	NReviews     int
}

func main() {
	c := colly.NewCollector(colly.AllowedDomains("books.toscrape.com"))

	c.OnRequest(func(r *colly.Request) {
		fmt.Printf("Visiting %s...\n", r.URL.String())
	})

	c.OnHTML("div.side_categories * > a", func(e *colly.HTMLElement) {
		e.Request.Visit(e.Attr("href"))
	})

	c.OnHTML("li.next > a", func(e *colly.HTMLElement) {
		e.Request.Visit(e.Attr("href"))
	})

	c.OnXML("//article[@class=\"product_pod\"]/h3/a", func(e *colly.XMLElement) {
		e.Request.Visit(e.Attr("href"))
	})

	c.OnResponse(func(r *colly.Response) {
		fmt.Printf("Visited %s\n", r.Request.URL)
	})

	c.Visit("https://books.toscrape.com")
}
