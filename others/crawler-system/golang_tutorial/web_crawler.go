package main

import (
	"fmt"
	"sync"
)

type Fetcher interface {
	// Fetch returns the body of URL and a slice of URLs found on that page
	Fetch(url string) (body string, urls []string, err error)
}

type UrlMap struct {
	mu sync.Mutex
	v  map[string]int
}

// Inc increments the counter for the given key
func (c *UrlMap) Set(key string) {
	c.mu.Lock()
	// Lock so only one goroutine at a time can access the map c.v
	defer c.mu.Unlock()
	c.v[key] = 0
}

// Value returns the current value of the counter for the given key
func (c *UrlMap) Exist(key string) bool {
	c.mu.Lock()
	// Lock so only one goroutine at a time can access the map c.v
	defer c.mu.Unlock()
	_, ok := c.v[key]
	fmt.Println(ok)
	return ok
}

// Crawl uses fetcher to recursively crawl pages starting with url
// to a maximum depth
func (cache *UrlMap) Crawl(url string, depth int, fetcher Fetcher) {
	// TODO: Fetch URLs in parallel
	// TODO: Don't fetch the same URL twice
	if cache.Exist(url) {
		return
	}
	if depth < 0 {
		return
	}
	body, urls, err := fetcher.Fetch(url)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("found: %s %q\n", url, body)
	for _, u := range urls {
		go cache.Crawl(u, depth-1, fetcher)
	}
	return
}

func main() {
	cache := UrlMap{}
	cache.Crawl("https://golang.org/", 4, fetcher)
}

// fakeFetcher is Fetcher that returns canned results.
type fakeFetcher map[string]*fakeResult

type fakeResult struct {
	body string
	urls []string
}

func (f fakeFetcher) Fetch(url string) (string, []string, error) {
	// Check if the url as key in the fake map or not
	if res, ok := f[url]; ok {
		return res.body, res.urls, nil
	}
	return "", nil, fmt.Errorf("not found: %s", url)
}

// fetcher is a populated fakeFetcher.
var fetcher = fakeFetcher{
	"https://golang.org/": &fakeResult{
		"The Go Programming Language",
		[]string{
			"https://golang.org/pkg/",
			"https://golang.org/cmd/",
		},
	},
	"https://golang.org/pkg/": &fakeResult{
		"Packages",
		[]string{
			"https://golang.org/",
			"https://golang.org/cmd/",
			"https://golang.org/pkg/fmt/",
			"https://golang.org/pkg/os/",
		},
	},
	"https://golang.org/pkg/fmt/": &fakeResult{
		"Package fmt",
		[]string{
			"https://golang.org/",
			"https://golang.org/pkg/",
		},
	},
	"https://golang.org/pkg/os/": &fakeResult{
		"Package os",
		[]string{
			"https://golang.org/",
			"https://golang.org/pkg/",
		},
	},
}
