package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/gocolly/colly"
)

type Book struct {
	Title        string
	Description  string
	UPC          string
	PriceExclTax float64
	PriceInclTax float64
	Availability string
	NReviews     int
}

func main() {
	c := colly.NewCollector(colly.AllowedDomains("books.toscrape.com"), colly.Async(true))

	c.OnRequest(func(r *colly.Request) {
		fmt.Printf("Visiting %s...\n", r.URL.String())
	})

	c.OnHTML("div.side_categories * > a", func(e *colly.HTMLElement) {
		e.Request.Visit(e.Attr("href"))
	})

	c.OnHTML("li.next > a", func(e *colly.HTMLElement) {
		e.Request.Visit(e.Attr("href"))
	})

	c.OnHTML("article.product_pod > h3 > a", func(e *colly.HTMLElement) {
		e.Request.Visit(e.Attr("href"))
	})

	c.OnXML("//article[.//div[@id=\"product_description\"]]", func(e *colly.XMLElement) {
		title := e.ChildText(".//h1")
		description := e.ChildText("./p")
		upc := e.ChildText(".//tr[./th[contains(text(), \"UPC\")]]/td")

		priceStrExclTax := e.ChildText(".//tr[./th[contains(text(), \"Price (excl. tax)\")]]/td")
		priceStrExclTax = strings.Replace(priceStrExclTax, "£", "", 1)
		priceExclTax, _ := strconv.ParseFloat(priceStrExclTax, 64)

		priceStrInclTax := e.ChildText(".//tr[./th[contains(text(), \"Price (incl. tax)\")]]/td")
		priceStrInclTax = strings.Replace(priceStrInclTax, "£", "", 1)
		priceInclTax, _ := strconv.ParseFloat(priceStrInclTax, 64)

		availability := e.ChildText(".//tr[./th[contains(text(), \"Availability\")]]/td")
		nReviews, _ := strconv.Atoi(e.ChildText(".//tr[./th[contains(text(), \"Number of reviews\")]]/td"))

		book := Book{
			Title:        title,
			Description:  description,
			UPC:          upc,
			PriceExclTax: priceExclTax,
			PriceInclTax: priceInclTax,
			Availability: availability,
			NReviews:     nReviews,
		}

		fmt.Println(book)
	})

	c.OnResponse(func(r *colly.Response) {
		fmt.Printf("Visited %s\n", r.Request.URL)
	})

	c.Visit("https://books.toscrape.com")
	c.Wait()
}
