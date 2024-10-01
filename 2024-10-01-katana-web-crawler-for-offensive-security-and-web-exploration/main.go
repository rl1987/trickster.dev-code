package main

import (
	"bytes"
	"log"
	"math"
	"strconv"

	"github.com/goccy/go-graphviz"
	"github.com/goccy/go-graphviz/cgraph"
	"github.com/projectdiscovery/gologger"
	"github.com/projectdiscovery/katana/pkg/engine/standard"
	"github.com/projectdiscovery/katana/pkg/output"
	"github.com/projectdiscovery/katana/pkg/types"
)

func main() {
	g := graphviz.New()
	graph, _ := g.Graph()
	defer func() {
		graph.Close()
		g.Close()
	}()

	nodes := map[string]*cgraph.Node{}

	options := &types.Options{
		MaxDepth:     3,               // Maximum depth to crawl
		FieldScope:   "rdn",           // Crawling Scope Field
		BodyReadSize: math.MaxInt,     // Maximum response size to read
		Timeout:      10,              // Timeout is the time to wait for request in seconds
		Concurrency:  10,              // Concurrency is the number of concurrent crawling goroutines
		Parallelism:  10,              // Parallelism is the number of urls processing goroutines
		Delay:        0,               // Delay is the delay between each crawl requests in seconds
		RateLimit:    150,             // Maximum requests to send per second
		Strategy:     "breadth-first", // Visit strategy (depth-first, breadth-first)
		OnResult: func(result output.Result) { // Callback function to execute for result
			referer := result.Request.Source

			if referer != "" {
				gologger.Info().Msg(referer + " -> " + result.Request.URL)
			} else {
				gologger.Info().Msg(result.Request.URL)
			}

			node, _ := graph.CreateNode(result.Request.URL)
			nodes[result.Request.URL] = node
			prevNode := nodes[referer]

			if prevNode != nil {
				e, _ := graph.CreateEdge("", prevNode, node)
				e.SetLabel(strconv.Itoa(result.Response.StatusCode))
			}
		},
	}
	crawlerOptions, err := types.NewCrawlerOptions(options)
	if err != nil {
		gologger.Fatal().Msg(err.Error())
	}
	defer crawlerOptions.Close()
	crawler, err := standard.New(crawlerOptions)
	if err != nil {
		gologger.Fatal().Msg(err.Error())
	}
	defer crawler.Close()
	var input = "https://public-firing-range.appspot.com/"
	err = crawler.Crawl(input)
	if err != nil {
		gologger.Warning().Msgf("Could not crawl %s: %s", input, err.Error())
	}

	var buf bytes.Buffer
	if err := g.Render(graph, "dot", &buf); err != nil {
		log.Fatal(err)
	}

	if err := g.RenderFilename(graph, graphviz.SVG, "katana.svg"); err != nil {
		log.Fatal(err)
	}

}
