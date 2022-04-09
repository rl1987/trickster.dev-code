package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"

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

func (b *Book) ToCSVRow() []string {
	return []string{
		b.Title,
		b.Description,
		b.UPC,
		fmt.Sprintf("%.2f", b.PriceExclTax),
		fmt.Sprintf("%.2f", b.PriceInclTax),
		b.Availability,
		fmt.Sprintf("%d", b.NReviews),
	}
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

	outF, err := os.OpenFile("books.csv", os.O_RDWR|os.O_CREATE, 0755)
	if err != nil {
		panic(err)
	}

	var mtx sync.Mutex

	csvWriter := csv.NewWriter(outF)
	csvWriter.Write([]string{"title", "description", "upc", "price_excl_tax", "price_incl_tax", "availability", "n_reviews"})

	c.OnXML("//article[@class=\"product_page\"]", func(e *colly.XMLElement) {
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

		mtx.Lock()
		fmt.Println(book)
		csvWriter.Write(book.ToCSVRow())
		mtx.Unlock()
	})

	c.OnResponse(func(r *colly.Response) {
		fmt.Printf("Visited %s\n", r.Request.URL)
	})

	c.Visit("https://books.toscrape.com")
	c.Wait()

	csvWriter.Flush()
	outF.Close()
}
